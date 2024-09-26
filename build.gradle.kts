/*
 * This file was generated by the Gradle 'init' task.
 */

plugins {
    `java-library`
    `maven-publish`
    id("com.gradleup.shadow") version "8.3.1"

}

repositories {
    mavenLocal()
    maven {
        url = uri("https://repo.maven.apache.org/maven2/")
    }
}

dependencies {
    api("net.sf.py4j:py4j:0.10.9")
    api("fr.inria.corese:corese-core:5.0.0-SNAPSHOT")
    api("jakarta.activation:jakarta.activation-api:2.1.2")
    api("info.picocli:picocli:4.7.5")
    testImplementation("junit:junit:4.13.2")
}

group = "fr.inria.corese"
version = "5.0.0-SNAPSHOT"
description = "corese-python"
java.sourceCompatibility = JavaVersion.VERSION_11

publishing {
    publications.create<MavenPublication>("maven") {
        from(components["java"])
    }
}

tasks.withType<JavaCompile>() {
    options.encoding = "UTF-8"
}

tasks.withType<Javadoc>() {
    options.encoding = "UTF-8"
}

tasks {
    shadowJar {
        this.archiveClassifier = "jar-with-dependencies"
    }
}
