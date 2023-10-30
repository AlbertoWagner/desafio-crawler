import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions, Keys

from desafio_crawler.settings import BASE_DIR


class WebMovieScraper:
    def __init__(self):
        self.logger = logging.getLogger("db")
        self.options = self._set_options()
        self.driver = webdriver.Firefox(options=self.options)
        self.waiting_seconds = 2

    def _set_options(self):
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.headless = True
        return options

    def _screenshot_pag_movie(self, cont):
        screenshot_file = f"{BASE_DIR}/scraping/screenshot/movie_screenshot_{cont}.png"
        self.driver.save_screenshot(screenshot_file)
        self.logger.info(f"Screenshot salva: {screenshot_file}")

    def _scrape_movie_info(self, movie):
        poster_url = movie.find("img").attrs["src"]
        list_title__text = movie.find(class_="ipc-title__text").text.split(".")
        title = list_title__text[-1].strip()
        rating = list_title__text[0].strip()
        metadata_list = movie.find(class_="cli-title-metadata").findAll("span")
        year = metadata_list[0].text.strip()
        duration = metadata_list[1].text.strip()

        movie_info = {
            "title": title,
            "rating": rating,
            "year": year,
            "duration": duration,
            "poster_url": poster_url,
        }

        return movie_info

    def run(self):
        IMDB_URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
        self.driver.get(IMDB_URL)
        while True:
            self._screenshot_pag_movie(1)
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(5)
            self._screenshot_pag_movie(2)
            if "© 1990-" in self.driver.page_source:  # Fim da pág
                break

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        movies = soup.find(class_="ipc-metadata-list--base").findAll("li")

        movie_data = []

        for movie in movies:
            movie_info = self._scrape_movie_info(movie)
            movie_data.append(movie_info)

        self.driver.quit()
        self.logger.info("Extração de dados concluída.")

        return movie_data
