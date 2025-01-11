#include <curl/curl.h>

#include <iostream>
#include <nlohmann/json.hpp>
#include <string>
#include <vector>

using json = nlohmann::json;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb,
                            void *userp) {
  ((std::string *)userp)->append((char *)contents, size * nmemb);
  return size * nmemb;
}

auto market_cap_api(std::string API_KEY, std::vector<std::string> stocks) {
  std::string stocks_str = "";
  for (int i = 0; i < stocks.size(); i++) {
    stocks_str += stocks[i];
    if (i != stocks.size() - 1) {
      stocks_str += ",";
    }
  }
  std::string url =
      "https://financialmodelingprep.com/api/v3/market-capitalization/" +
      stocks_str + "?apikey=" + API_KEY;
  CURL *curl;
  CURLcode res;
  std::string readBuffer;
  curl = curl_easy_init();
  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER,
                     false);  // workaround for Windows, I have no idea how to
                              // config libcurl use windows's certificate store
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, false);
    res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
  }
  return json::parse(readBuffer);
}

auto historical_market_cap_api(std::string API_KEY, std::string stock,
                               std::string _from, std::string to, int limit) {
  std::string url =
      "https://financialmodelingprep.com/api/v3/"
      "historical-price-full/" +
      stock + "?limit=" + std::to_string(limit) + "&from=" + _from +
      "&to=" + to + "&apikey=" + API_KEY;
  CURL *curl;
  CURLcode res;
  std::string readBuffer;
  curl = curl_easy_init();
  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, false);
    res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
  }
  return json::parse(readBuffer);
}

int main() {
  std::string API_KEY = std::getenv("API_KEY");
  std::cout << API_KEY << std::endl;
  std::cout << market_cap_api(API_KEY, {"AAPL", "GOOGL"}) << std::endl;
  std::cout << historical_market_cap_api(API_KEY, "AAPL", "2021-01-01",
                                         "2021-01-10", 10)
            << std::endl;
  return 0;
}