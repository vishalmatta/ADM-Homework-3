from bs4 import BeautifulSoup
import requests,csv,re,time
from collections import defaultdict
import numpy as np
import pandas as pd

def get_movie_tsv():
    total_list = []
    for _ in range(10):
        file_name = _
        file_name_1 = r"C:\Users\Gabriele\Desktop\MOVIES_D\article-" + str(_) + ".html"

        with open(r"C:\Users\Gabriele\Desktop\MOVIES_D\article-" + str(_) + ".html", encoding="utf8") as f:
            movie = f.read()
            soup = BeautifulSoup(movie, 'html.parser')
        table = soup.find("table", {"class": "infobox vevent"})
        subj = ['Directed by', 'Produced by', 'Written by', 'Starring', 'Music by', 'Release date', 'Running time',
                'Country', 'Language', 'Budget']

        def title():
            try:
                return soup.select("h1")[0].i.text
            except:
                return soup.select("h1")[0].text

        dict = defaultdict(lambda: [])
        try:
            for _ in range(len(table.find_all("th"))):
                head = table.find_all("th")[_].text
                value = table.find_all("td")[_]
                buffer = value.find_all(text=True)
                string = " ".join(buffer)
                dict[head].append(string)
        except:
            pass
        try:
            intro = soup.select(".mw-parser-output")[0]
        except:
            intro = "NA"
            pass
        intro_str = ""
        plot_str = ""
        tag_list = []
        try:
            for child in intro.recursiveChildGenerator():
                if child.name == "p":
                    intro_str += "".join(child.text.strip("\n"))
                if child.name == "h2":
                    break
        except:
            pass
        # collect plot in this list
        try:
            plot = []
            # find the node with id of "Plot"
            mark = soup.find(id="Plot_summary")
            if mark == None:
                mark = soup.find(id="Plot")
            if mark == None:
                mark = soup.find(id="Plot_Summary")

            # walk through the siblings of the parent (H2) node
            # until we reach the next H2 node
            for elt in mark.parent.nextSiblingGenerator():
                if elt.name == "h2":
                    break
                if hasattr(elt, "text"):
                    plot.append(elt.text)

            plot_str = "".join(plot).strip("\n")
        except:
            plot = "NA"
            pass
        try:
            name = table.find("th", attrs={"class": "summary"}).text
        except:
            name = "NA"

        def wrapper(string):
            try:
                b = dict[string][0]
                return b
            except IndexError:
                return "NA"

        url_name = soup.find("a", attrs={"class": "group-21"}).text
        wrapper_list = []
        wrapper_list.append(title())
        wrapper_list.append(intro_str)
        wrapper_list.append(plot_str)
        wrapper_list.append(name)
        for _ in subj:
            w = wrapper(_)
            wrapper_list.append(w)
        try:
            wrapper_list[9] = wrapper_list[9].strip().split()[0]
        except:
            wrapper_list[9] = "NA"
        # wrapper_list is a list of all elements we want to create tsv from.
        return_list = [wrapper_list[0], wrapper_list[1], url_name, file_name_1]
        total_list.append(return_list)
        with open(r"C:\Users\Gabriele\Desktop\tsv\article-" + str(_) + ".tsv", 'wt', encoding="utf8") as write_tsv:
            tsv_writer = csv.writer(write_tsv, delimiter='\t')
            tsv_writer.writerow(wrapper_list)
    return total_list

get_movie_tsv()