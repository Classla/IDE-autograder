import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.TestIdentifier;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;
import org.junit.platform.launcher.listeners.TestExecutionSummary;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;

import java.io.PrintWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Set;
import java.util.stream.Collectors;

import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;

public class UnitTestDriver {
    public static void main(String[] args) {

        // Create a LauncherDiscoveryRequestBuilder
        LauncherDiscoveryRequestBuilder requestBuilder = LauncherDiscoveryRequestBuilder.request();

        // Dynamically add test classes from the command-line arguments
        for (String className : args) {
            requestBuilder.selectors(selectClass(className));
        }

        // Build the request
        LauncherDiscoveryRequest request = requestBuilder.build();

        Launcher launcher = LauncherFactory.create();
        SummaryGeneratingListener listener = new SummaryGeneratingListener();

        // Retrieve and print the list of test classes
        Set<TestIdentifier> testIdentifiers = launcher.discover(request).getRoots();
        Set<String> testClasses = testIdentifiers.stream()
                .map(TestIdentifier::getDisplayName)
                .collect(Collectors.toSet());

        System.out.println("Detected test classes:");
        testClasses.forEach(System.out::println);

        launcher.execute(request, listener);

        TestExecutionSummary summary = listener.getSummary();
        summary.printTo(new PrintWriter(System.out));

        long testsPassed = summary.getTestsSucceededCount();
        long totalTests = summary.getTestsFoundCount();

        try (FileWriter writer = new FileWriter("num_tests_passed.txt")) {
            writer.write(Long.toString(testsPassed));
        } catch (IOException e) {
            e.printStackTrace();
        }

        try (FileWriter writer = new FileWriter("num_tests.txt")) {
            writer.write(Long.toString(totalTests));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
