import java.security.interfaces.*;
import java.util.Date;
import javax.crypto.*;

import com.nimbusds.jose.*;
import com.nimbusds.jose.crypto.*;
import com.nimbusds.jwt.*;


// RSA signatures require a public and private RSA key pair, the public key 
// must be made known to the JWS recipient in order to verify the signatures
KeyPairGenerator keyGenerator = KeyPairGenerator.getInstance("RSA");
keyGenerator.initialize(1024);

KeyPair kp = keyGenerator.genKeyPair();
RSAPublicKey publicKey = (RSAPublicKey)kp.getPublic();
RSAPrivateKey privateKey = (RSAPrivateKey)kp.getPrivate();

// Create RSA-signer with the private key
JWSSigner signer = new RSASSASigner(privateKey);

// Prepare JWT with claims set
JWTClaimsSet claimsSet = new JWTClaimsSet();
claimsSet.setSubject("alice");
claimsSet.setIssuer("https://c2id.com");
claimsSet.setExpirationTime(new Date(new Date().getTime() + 60 * 1000));

SignedJWT signedJWT = new SignedJWT(
    new JWSHeader(JWSAlgorithm.RS256), 
    claimsSet);

// Compute the RSA signature
signedJWT.sign(signer);

// To serialize to compact form, produces something like
// eyJhbGciOiJSUzI1NiJ9.SW4gUlNBIHdlIHRydXN0IQ.IRMQENi4nJyp4er2L
// mZq3ivwoAjqa1uUkSBKFIX7ATndFF5ivnt-m8uApHO4kfIFOrW7w2Ezmlg3Qd
// maXlS9DhN0nUk_hGI3amEjkKd0BWYCB8vfUbUv0XGjQip78AI4z1PrFRNidm7
// -jPDm5Iq0SZnjKjCNS5Q15fokXZc8u0A
String s = signedJWT.serialize();

// On the consumer side, parse the JWS and verify its RSA signature
signedJWT = SignedJWT.parse(s);

JWSVerifier verifier = new RSASSAVerifier(publicKey);
assertTrue(signedJWT.verify(verifier));

// Retrieve / verify the JWT claims according to the app requirements
assertEquals("alice", signedJWT.getJWTClaimsSet().getSubject());
assertEquals("https://c2id.com", signedJWT.getJWTClaimsSet().getIssuer());
assertTrue(new Date().before(signedJWT.getJWTClaimsSet().getExpirationTime());
