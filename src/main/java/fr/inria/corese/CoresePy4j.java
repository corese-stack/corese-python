package fr.inria.corese;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Optional;

import fr.inria.corese.core.util.Property;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Model.CommandSpec;
import picocli.CommandLine.Option;
import picocli.CommandLine.Spec;
import py4j.GatewayServer;

/**
 * This class provides a command-line interface for running CoresePy4j.
 * It listens on a specified port and provides a gateway server for Python
 * programs to interact with Corese.
 */
@Command(name = "Corese-python", version = "4.4.1", mixinStandardHelpOptions = true)
public class CoresePy4j implements Runnable {

    /**
     * The command-line specification.
     */
    @Spec
    CommandSpec spec;

    /**
     * The port number to listen on.
     */
    @Option(names = { "-p", "--port" }, description = "Port to listen on", defaultValue = "25333")
    private static int port;

    /**
     * The path to the configuration file.
     */
    @Option(names = { "-c", "--config",
            "--init" }, description = "Path to a configuration file. If not provided, the default configuration file will be used.", required = false)
    private Path configFilePath;

    /**
     * The main method that starts the CoresePy4j gateway server.
     * 
     * @param args The command-line arguments.
     */
    public static void main(String[] args) {
        new CommandLine(new CoresePy4j()).execute(args);
    }

    @Override
    public void run() {
        loadConfigFile();
        startGatewayServer();
    }

    /**
     * Loads the configuration file.
     */
    private void loadConfigFile() {
        Optional<Path> configFilePath = Optional.ofNullable(this.configFilePath);
        if (configFilePath.isPresent()) {
            Path path = configFilePath.get();
            try {
                Property.load(path.toString());
                spec.commandLine().getErr().println("Loaded config file: " + path.toString());
            } catch (IOException e) {
                spec.commandLine().getErr().println("Failed to load config file: " + path.toString());
                e.printStackTrace();
                System.exit(1);
            }
        } else {
            spec.commandLine().getErr().println("Loaded default config");
        }
    }

    /**
     * Starts the gateway server.
     */
    private void startGatewayServer() {
        GatewayServer gatewayServer = new GatewayServer(new CoresePy4j(), port);
        gatewayServer.start();
        spec.commandLine().getOut().println("CoresePy4j gateway server started on port " + port);
    }

}
