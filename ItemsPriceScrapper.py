import yaml
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os

def get_url_list(yaml_file_path):
    url_list = []
    
    with open(yaml_file_path) as file:
        url_list = yaml.safe_load(file)
    
    return url_list 


def save_to_csv(database_name, df_to_be_written):
    if os.path.isfile(database_name):
        df1 = pd.read_csv(database_name)
        df2 = pd.concat([df1, df_to_be_written], ignore_index=True)
        df2.reset_index()
        df2.to_csv(database_name, index=False)
    else:
        df_to_be_written.to_csv(database_name, index=False)
    
    
def get_data_from_browser(wait_time, url_list):
    if not url_list:
        raise Exception('YAML is empty!')
    # in seconds
    # firefox_options = Options().add_argument()
    driver = webdriver.Firefox()
    # driver.minimize_window()
    items_list = []

    for url in url_list:
        driver.get(url)
        time.sleep(wait_time)

        # write for implicit wait 
        current_date_time = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S')
        item_name = driver.find_element('xpath', '//*[@id="productTitle"]').text

        for i in driver.find_elements('xpath', '//*[@class="a-price-whole"]'):
            if len(i.text) > 0:
                item_price = int(''.join(i.text.split(',')))
    #             print(item_name, item_price, current_date_time)

                d = {'Item Name': item_name, 'Item Price': item_price, 'Added Date': current_date_time}
                items_list.append(d)
                break

    driver.close()
    
    df = pd.DataFrame(items_list)
    return df

    
def main():
    YAML_FILE_PATH = 'items_link.yaml'
    DATABASE_NAME = 'database.csv'
    WAIT_TIME = 5
    
    if not os.path.isfile(YAML_FILE_PATH):
        open(YAML_FILE_PATH, mode='w')
        raise Exception('Yaml file not present! Created one.')
    
    url_list = get_url_list(YAML_FILE_PATH)
    result_dataframe = get_data_from_browser(WAIT_TIME, url_list)
    save_to_csv(database_name=DATABASE_NAME, df_to_be_written=result_dataframe)
    

if __name__ == '__main__':
    main()