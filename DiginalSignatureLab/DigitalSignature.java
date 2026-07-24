package DiginalSignature;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Signature;
import java.security.spec.X509EncodedKeySpec;

// imports for PDFBox signing (loaded via reflection)
import java.io.InputStream;
import java.util.Calendar;

/**
 * A simple Java program that demonstrates how to create a digital signature for a PDF
 *
 * The implementation follows the Oracle tutorial for the Java Cryptography API
 * (see https://docs.oracle.com/javase/tutorial/security/apisign/index.html).
 */
public class DigitalSignature {

    public static void main(String[] args) {
        try {
            // debugging: if invoked with --print-methods, show PDDocument methods
            for (String arg : args) {
                if ("--print-methods".equals(arg)) {
                    try {
                        Class<?> pdDocClass = Class.forName("org.apache.pdfbox.pdmodel.PDDocument");
                        System.out.println("Methods in PDDocument:");
                        for (java.lang.reflect.Method m : pdDocClass.getMethods()) {
                            System.out.println("  " + m);
                        }
                    } catch (ClassNotFoundException cnf) {
                        System.out.println("PDDocument class not found on classpath");
                    }                    try {
                        Class<?> loaderClass = Class.forName("org.apache.pdfbox.Loader");
                        System.out.println("Methods in Loader:");
                        for (java.lang.reflect.Method m : loaderClass.getMethods()) {
                            System.out.println("  " + m);
                        }
                    } catch (ClassNotFoundException cnf) {
                        System.out.println("Loader class not found on classpath");
                    }
                    try {
                        Class<?> pdSigClass = Class.forName("org.apache.pdfbox.pdmodel.interactive.digitalsignature.PDSignature");
                        System.out.println("Methods in PDSignature:");
                        for (java.lang.reflect.Method m : pdSigClass.getMethods()) {
                            System.out.println("  " + m);
                        }
                        System.out.println("Fields in PDSignature:");
                        for (java.lang.reflect.Field f : pdSigClass.getFields()) {
                            System.out.println("  " + f);
                        }
                    } catch (ClassNotFoundException cnf) {
                        System.out.println("PDSignature class not found on classpath");
                    }
                    return;
                }
            }
            Path workingDir = Paths.get(".").toAbsolutePath().normalize();
            System.out.println("Working directory: " + workingDir);

            Path pdf = workingDir.resolve("Pdf a firmar.pdf");
            if (!Files.exists(pdf)) {
                System.err.println("Sample PDF file not found: " + pdf);
                System.exit(1);
            }

            // generate key pair
            KeyPair keyPair = generateKeyPair();

            // save public key
            Path pubKeyFile = workingDir.resolve("public.key");
            savePublicKey(keyPair.getPublic(), pubKeyFile.toFile());

            // sign the pdf file
            byte[] signatureBytes = signFile(pdf.toFile(), keyPair.getPrivate());
            Path sigFile = workingDir.resolve("signature.sig");
            try (FileOutputStream fos = new FileOutputStream(sigFile.toFile())) {
                fos.write(signatureBytes);
            }

            System.out.println("Generated files:");
            System.out.println("   Public key -> " + pubKeyFile);
            System.out.println("   Signature  -> " + sigFile);

            // attempt to create a new PDF containing the signature if PDFBox is on classpath
            try {
                File signedPdf = workingDir.resolve("Pdf a firmar_signed.pdf").toFile();
                createSignedPdfWithPdfBox(pdf.toFile(), keyPair.getPrivate(), signedPdf);
                System.out.println("   Signed PDF -> " + signedPdf);
            } catch (NoClassDefFoundError | ClassNotFoundException cnfe) {
                System.out.println("PDFBox not found; skipping embedded PDF signing.");
            }


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static KeyPair generateKeyPair() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        keyGen.initialize(2048);
        return keyGen.generateKeyPair();
    }

    private static void savePublicKey(PublicKey pubKey, File outFile) throws IOException {
        byte[] encoded = pubKey.getEncoded();
        try (FileOutputStream fos = new FileOutputStream(outFile)) {
            fos.write(encoded);
        }
    }

    private static byte[] signFile(File inputFile, PrivateKey privateKey) throws Exception {
        byte[] data = Files.readAllBytes(inputFile.toPath());
        Signature signer = Signature.getInstance("SHA256withRSA");
        signer.initSign(privateKey);
        signer.update(data);
        return signer.sign();
    }

    /**
     * Optional helper that can be used to verify the signature using the saved public
     * key. Not invoked from main by default, but provided for completeness.
     */
    public static boolean verifySignature(File inputFile, File signatureFile, File publicKeyFile) throws Exception {
        byte[] data = Files.readAllBytes(inputFile.toPath());
        byte[] sigBytes = Files.readAllBytes(signatureFile.toPath());
        byte[] pubKeyBytes = Files.readAllBytes(publicKeyFile.toPath());

        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(pubKeyBytes);
        PublicKey pubKey = KeyFactory.getInstance("RSA").generatePublic(keySpec);

        Signature verifier = Signature.getInstance("SHA256withRSA");
        verifier.initVerify(pubKey);
        verifier.update(data);
        return verifier.verify(sigBytes);
    }

    // ------------------------------------------------------------------
    // PDF signing support (requires external library PDFBox)
    // ------------------------------------------------------------------

    public static void createSignedPdfWithPdfBox(File srcPdf,
            final PrivateKey signingKey, File destPdf) throws Exception {
        // reflection-based implementation that works with any PDFBox version
        Class<?> loaderClass = Class.forName("org.apache.pdfbox.Loader");
        Class<?> pdDocClass = Class.forName("org.apache.pdfbox.pdmodel.PDDocument");
        Class<?> pdSigClass = Class.forName("org.apache.pdfbox.pdmodel.interactive.digitalsignature.PDSignature");
        Class<?> sigIfaceClass = Class.forName("org.apache.pdfbox.pdmodel.interactive.digitalsignature.SignatureInterface");
        Class<?> sigOptsClass = Class.forName("org.apache.pdfbox.pdmodel.interactive.digitalsignature.SignatureOptions");

        // choose the simplest overload: one parameter File
        java.lang.reflect.Method loadMethod = null;
        for (java.lang.reflect.Method m : loaderClass.getMethods()) {
            if (m.getName().equals("loadPDF") && java.lang.reflect.Modifier.isStatic(m.getModifiers())) {
                Class<?>[] params = m.getParameterTypes();
                if (params.length == 1 && params[0].equals(File.class)) {
                    loadMethod = m;
                    break;
                }
            }
        }
        if (loadMethod == null) {
            // fallback: just pick any static loadPDF and plan to supply nulls
            for (java.lang.reflect.Method m : loaderClass.getMethods()) {
                if (m.getName().equals("loadPDF") && java.lang.reflect.Modifier.isStatic(m.getModifiers())) {
                    loadMethod = m;
                    break;
                }
            }
        }
        if (loadMethod == null) {
            throw new NoSuchMethodException("no Loader.loadPDF methods found");
        }

        Object document;
        if (loadMethod.getParameterCount() == 1) {
            document = loadMethod.invoke(null, srcPdf);
        } else {
            // pad remaining args with null or defaults
            Object[] args = new Object[loadMethod.getParameterCount()];
            args[0] = srcPdf;
            for (int i = 1; i < args.length; i++) {
                args[i] = null;
            }
            document = loadMethod.invoke(null, args);
        }

        Object sig = pdSigClass.getConstructor().newInstance();
        Class<?> cosNameClass = Class.forName("org.apache.pdfbox.cos.COSName");
        // FILTER_ADOBE_PPKLITE and SUBFILTER_ADBE_PKCS7_SHA256 areCOSName constants
        pdSigClass.getMethod("setFilter", cosNameClass).invoke(sig,
                pdSigClass.getField("FILTER_ADOBE_PPKLITE").get(null));
        // SHA256 constant not present in 3.0.6; use generic PKCS7 detached
        pdSigClass.getMethod("setSubFilter", cosNameClass).invoke(sig,
                pdSigClass.getField("SUBFILTER_ADBE_PKCS7_DETACHED").get(null));
        pdSigClass.getMethod("setName", String.class).invoke(sig, "Signed by Java program");
        pdSigClass.getMethod("setLocation", String.class).invoke(sig, "Localhost");
        pdSigClass.getMethod("setReason", String.class).invoke(sig, "Document approval");
        pdSigClass.getMethod("setSignDate", Calendar.class).invoke(sig, Calendar.getInstance());

        Object options = sigOptsClass.getConstructor().newInstance();
        int defaultSize = sigOptsClass.getField("DEFAULT_SIGNATURE_SIZE").getInt(null);
        sigOptsClass.getMethod("setPreferredSignatureSize", int.class).invoke(options, defaultSize * 2);

        Object handler = java.lang.reflect.Proxy.newProxyInstance(
                sigIfaceClass.getClassLoader(),
                new Class[]{sigIfaceClass},
                (proxy, method, args) -> {
                    if ("sign".equals(method.getName())) {
                        InputStream content = (InputStream) args[0];
                        Signature signature = Signature.getInstance("SHA256withRSA");
                        signature.initSign(signingKey);
                        byte[] buffer = content.readAllBytes();
                        signature.update(buffer);
                        return signature.sign();
                    }
                    throw new UnsupportedOperationException("Unexpected method: " + method);
                });

        pdDocClass.getMethod("addSignature", pdSigClass, sigIfaceClass, sigOptsClass)
                .invoke(document, sig, handler, options);

        try (FileOutputStream fos = new FileOutputStream(destPdf)) {
            pdDocClass.getMethod("saveIncremental", java.io.OutputStream.class).invoke(document, fos);
        }
        pdDocClass.getMethod("close").invoke(document);
    }
}


