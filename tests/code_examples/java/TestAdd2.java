import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class TestAdd2 {

    @Test
    public void testAdd() {
        assertEquals(3, Add.add(1, 2));
        assertEquals(0, Add.add(-1, 1));
        assertEquals(-2, Add.add(-1, -1));
    }

    @Test
    public void testAddZero() {
        assertEquals(0, Add.add(0, 0));
        assertEquals(5, Add.add(0, 5));
        assertEquals(5, Add.add(5, 0));
    }
}
