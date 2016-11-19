import datetime
import time
import sys
import os
from url_checker.validator import check_if_url


class Generate_table(object):
    def __init__(self, table_dict):
        self.table_title = table_dict["table_title"]
        self.generate_sn = table_dict["generate_sn"]
        self.generate_summary = table_dict["generate_summary"]
        self.table_header = table_dict["table"][0]
        self.table_rows = table_dict["table"][1:]
        self.table_text = table_dict["table_text"]
        # Set encoding
        reload(sys)
        sys.setdefaultencoding('utf8')

    # Functions to generate table HTML
    def title(self):
        table_title = self.table_title
        if table_title == "":
            return ""
        else:
            return "<h4 class='title_wrapper'>" + table_title + "</h4>"

    def summary(self):
        column_to_summarise = str(self.generate_summary).lower()
        if column_to_summarise == "" or not self.generate_summary:
            return ""
        else:
            header_list = [header.lower() for header in self.table_header]
            # Find index of column with header stated
            col_to_summarise = None
            for col in range(len(header_list)):
                if header_list[col] == column_to_summarise:
                    col_to_summarise = col
                else:
                    pass

            if col_to_summarise is None:
                # Raise exception if header stated is not found
                print str('"' + column_to_summarise + '" not found in table headers')
            else:
                table_rows = self.table_rows
                total_all = len(table_rows)
                list_of_col_values = []
                for row in table_rows:
                    list_of_col_values += [row[col_to_summarise]]
                uniques = list(set(list_of_col_values))

                html = "<p><b>Total</b> : " + str(total_all) + "&nbsp;&nbsp;&nbsp;|| "
                for unique_value in uniques:
                    html += " " + str(unique_value) + " : " + str(list_of_col_values.count(unique_value)) + " ,"
                if html[-1] == ",":
                    html = html[:-1]
                    html += " ||</p>"
                else:
                    html += " ||</p>"
        return html

    def generate_table_header(self):
        headers_html = "<tr>"
        for i in self.table_header:
            headers_html += '<th>' + str(i) + '</th>'
        headers_html += "</tr>"
        return headers_html

    def check_table_for_urls(self, table_rows):
        table = table_rows
        for row in range(len(table)):
            for col in range(len(table[row])):
                table[row][col] = check_if_url().if_url_convert(table[row][col])
        return table

    def generate_table_row(self, row):
        row_html = "<tr>"
        for i in range(len(row)):
            row_html += "<td>" + str(row[i]) + "</td>"
        row_html += "</tr>"
        return row_html

    def generate_table_rows(self):
        table_rows = self.check_table_for_urls(self.table_rows)
        table_rows_html = ""
        for row in table_rows:
            table_rows_html += self.generate_table_row(row)
        return table_rows_html

    def generate_table_text(self):
        table_text = self.table_text
        if table_text == "":
            return ""
        else:
            return '<p>&nbsp;' + check_if_url().if_url_convert(table_text) + '</p>'

    def table(self):
            # removed table title before <table style> - <p style="font-weight: bold;">'+table_title+'</p>
            return '<p><table class="table_wrapper">' + self.generate_table_header() + self.generate_table_rows() +'</table></p>' + self.generate_table_text() + '<br/>'

    def as_html(self):
        if len(self.table_rows) == 0:
            pass
        else:
            return self.title() + self.summary() + self.table()


class Generate_email(object):
    def __init__(self, header, list_of_table_dicts, unsubscribe_mailto=""):
        self.email_header = header
        self.unsubscribe_mailto = unsubscribe_mailto
        self.table_dicts = list_of_table_dicts

    def html(self):
        if len(self.table_dicts) == 0:
            pass
        else:
            all_tables_in_html = ""
            for table in self.table_dicts:
                if len(table) == 0:
                    pass
                else:
                    all_tables_in_html += Generate_table(table).as_html()
            with open(os.path.dirname(__file__) + "/template/email.html", "r") as f:
                template = f.read().replace('\n', '')

            html_email = template.replace("*<-- EMAIL HEADER HERE -->*", self.email_header).replace("*<-- TABLES HERE -->*", all_tables_in_html).replace("*<-- UNSUBSCRIBE MAIL_TO HERE -->*", self.unsubscribe_mailto)
            return html_email

# Test case
if __name__ == '__main__':
    test_table_dict1 = {
        "table_title": "Family Members",
        "table_text": "http://www.ancestry.com/",
        "generate_sn": False,
        "generate_summary": "Gender",
        "table":
            [
                ["s/n", "Name", "Gender", "Age"],
                [1, "John", "M", "http://www.example.com"],
                [2, "Lucy", "F", "13"],
                [3, "Jack", "M", "64"]
            ]
    }
    test_table_dict2 = {
        "table_title": "Ancestors",
        "table_text": "Who knew a kid from Queens was descended from royalty?",
        "generate_sn": False,
        "generate_summary": "gender",
        "table":
            [
                ["s/n", "Name", "Gender", "Age"],
                [1, "John", "M", "23"],
                [2, "Lucy", "F", "13"],
                [3, "Jack", "M", "64"],
                [4, "Jack", "M", "64"]
            ]
    }
    list_of_table_dicts = [test_table_dict1, test_table_dict2]
    # Test generate table function
    print Generate_table(test_table_dict2).as_html()
    # Test generate email html function
    # print Generate_email("Daily report",list_of_table_dicts).html()
