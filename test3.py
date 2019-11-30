
__Author__ = "Soumil Nitin Shah"
__Version__ = '1.1.1'
__Email__ = "soushah@my.bridgeport.edu"


try:
    import requests
    import bs4
    from bs4 import BeautifulSoup
    import pandas as pd

except Exception as e:
    print("Some Modules are Missing {}".format(e))


class WebCrawler(object):

    def __init__(self, title = '',location = ""):

        self._url = "https://www.indeed.com/jobs"
        self._headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        self._title = title
        self._location = location
        self.params = {
            'q': 'Python',
            'l': 'Bridgeport, CT'}

    def get(self):

        try:

            r = requests.get(url=self._url,
                              headers=self._headers ,
                              params=self.params)
            return r.text

        except Exception as e:

            print("Failed to make response to Indeed")



class DataStructure():

    def __init__(self):
        self.data = {
            'title':[],
            'location':[],
            'summary':[],
            'date':[],
            'link':[]
        }




class DataCleaning(object):

    def __init__(self, title = '', location = ""):
        self._title = title
        self._location = location
        self._webcrawler = WebCrawler(self._title, self._location)
        self.data = self._webcrawler.get()
        self.datastructure = DataStructure()

    def getData(self):
        soup = BeautifulSoup(self.data, 'html.parser')

        for x in soup.findAll('div', class_="jobsearch-SerpJobCard unifiedRow row result"):

            title = x.find(class_="title").text.strip()
            self.datastructure.data["title"].append(title)


            location = x.find(class_="location accessible-contrast-color-location").text.strip()
            self.datastructure.data["location"].append(location)


            summary = x.find(class_="summary")
            self.datastructure.data["summary"].append(summary.text)

            date = x.find(class_="date")
            self.datastructure.data["date"].append(date)


            link = x.find('a', href=True)
            base_url = "https://www.indeed.com/"


            Final = base_url + link["href"]

            self.datastructure.data["link"].append(Final)


        data = list(zip(
            self.datastructure.data["title"],  self.datastructure.data["location"],
            self.datastructure.data["summary"],self.datastructure.data["date"],
            self.datastructure.data["link"]
        ))

        df = pd.DataFrame(data=data, columns=["title", "location", "summary", "date", "link" ])
        return df




class IndeedJobSearch(object):

    def __init__(self, title = '', location = ""):

        self.title = title
        self.location = location
        self.datacleaning = DataCleaning(title=self.title, location=self.location)

    def getJobs(self):
        data = self.datacleaning.getData()
        return data

    def saveCsv(self):

        data = self.datacleaning.getData()
        data.to_csv("Jobs.csv")

    def saveExcel(self):

        data = self.datacleaning.getData()
        data.to_excel("job.xls")



if __name__ == "__main__":

    jobsearch = IndeedJobSearch(title='Python', location="Bridgeport , CT")
    data  = jobsearch.getJobs()
    print(data)
    # jobsearch.saveExcel()
    #jobsearch.saveCsv()






