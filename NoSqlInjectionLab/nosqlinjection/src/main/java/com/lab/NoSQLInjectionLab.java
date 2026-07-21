package com.lab;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.FindIterable;
import org.bson.Document;
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.io.OutputStream;
import java.net.URLDecoder;

public class NoSQLInjectionLab {
    public static void main(String[] args) throws Exception {
        // 1. Conexión a tu MongoDB local y preparación de datos
        MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017");
        MongoDatabase database = mongoClient.getDatabase("lab_seguridad");
        MongoCollection<Document> users = database.getCollection("usuarios");

        // Limpiamos la colección e insertamos datos ficticios
        users.drop();
        users.insertOne(new Document("username", "admin")
                .append("password", "super_secreto_admin")
                .append("role", "ADMIN"));
        users.insertOne(new Document("username", "nicolas")
                .append("password", "12345")
                .append("role", "USER"));

        // 2. Creación del Servidor API en el puerto 8080
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        server.createContext("/buscar", exchange -> {
            String query = exchange.getRequestURI().getQuery();
            String userInput = "";
            
            // Extraemos y decodificamos lo que el usuario envía en la URL
            if (query != null && query.startsWith("user=")) {
                userInput = query.substring(5);
                userInput = URLDecoder.decode(userInput, "UTF-8");
            }

            // ¡AQUÍ ESTÁ LA VULNERABILIDAD! 
            // Concatenación directa de texto dentro de una evaluación JavaScript ($where)
            String jsQuery = "this.username == '" + userInput + "'";
            Document vulnQuery = new Document("$where", jsQuery);

            StringBuilder response = new StringBuilder("--- Resultados de Busqueda ---\n");

            try {
                // Ejecutamos la consulta en MongoDB
                FindIterable<Document> results = users.find(vulnQuery);
                for (Document doc : results) {
                    response.append(doc.toJson()).append("\n");
                }
            } catch (Exception e) {
                response.append("Error en la consulta BD.");
            }

            // Devolvemos la respuesta al navegador
            byte[] bytes = response.toString().getBytes();
            exchange.sendResponseHeaders(200, bytes.length);
            OutputStream os = exchange.getResponseBody();
            os.write(bytes);
            os.close();
        });

        server.start();
        System.out.println("Base de datos preparada.");
        System.out.println("API vulnerable corriendo en http://localhost:8080/buscar");
    }
}