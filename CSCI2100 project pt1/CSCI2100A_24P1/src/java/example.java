import java.util.List;
import java.util.Arrays;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import com.google.gson.Gson;


public class example {
    public static List<String> marketCapApi(String apiKey, List<String> stocks) {
        String stocksStr = String.join(",", stocks);
        String url = "https://financialmodelingprep.com/api/v3/market-capitalization/" + stocksStr + "?apikey=" + apiKey;
        try {
            URL urlObj = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) urlObj.openConnection();

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();

            return new Gson().fromJson(response.toString(), List.class);
        } catch (IOException e) {
            return null;
        }
    }

    public static List<String> historicalMarketCapApi(String apiKey, String stock, String from, String to, int limit) {
        String url = "https://financialmodelingprep.com/api/v3/historical-market-capitalization/" + stock + "?limit=" + limit + "&from=" + from + "&to=" + to + "&apikey=" + apiKey;
        try {
            URL urlObj = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) urlObj.openConnection();

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            reader.close();

            return new Gson().fromJson(response.toString(), List.class);
        } catch (IOException e) {
            return null;
        }
    }
    public static void main(String[] args) {
        String apiKey = System.getenv("API_KEY");
        List<String> stocks = Arrays.asList("AAPL", "GOOGL", "AMZN");
        List<String> marketCaps = marketCapApi(apiKey, stocks);
        System.out.println(marketCaps);

        List<String> historicalMarketCaps = historicalMarketCapApi(apiKey, "AAPL", "2020-01-01", "2020-12-31", 10);
        System.out.println(historicalMarketCaps);
    }
}