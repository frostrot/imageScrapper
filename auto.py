from selenium import webdriver
import os
import requests
import io
from PIL import Image
import hashlib

def image_scraper(wd,image_types:list,amount:int):
	for item in image_types:
		google_image_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
		wd.get(google_image_url.format(q=item))
		image_urls = set()
		image_count=0

		while image_count<amount:
			wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
			thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
			number_results = len(thumbnail_results)

			for img in thumbnail_results:
				try:
					img.click()
				except Exception:
					continue
				actual_img = wd.find_elements_by_css_selector('img.n3VNCb')

				for image in actual_img:
					if image.get_attribute('src') and 'http' in img.get_attribute('src'):
						image_urls.add(image.get_attribute('src'))
				image_count = len(image_urls)
				if image_count>=amount:
					print(f"Found: {image_count} images of {item} links, Done!")
					break
			else:
				print("Found:", {image_count},f"image links of {item}, looking for more...")
				load_more = wd.find_elements_by_css_selector(".MidC8d")
				if load_more:
					load_more.click()
		parse_url(item,image_urls)
	return
def parse_url(name:str,urls: set):
	target_path = "./images"
	target_folder = os.path.join(target_path,'_'.join(name.lower().split(" ")))
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)
	for i,url in enumerate(urls):		
		try:
			image_content = requests.get(url).content
		except Exception as e:
			print(f"Error - Could not Download image no. {i} of {name}.")
			continue

		try:
			image_file = io.BytesIO(image_content)
			image = Image.open(image_file).convert('RGB')
			file_path = os.path.join(target_folder,hashlib.sha1(image_content).hexdigest()[:10]+'.jpg')
			with open(file_path,'wb') as f:
				image.save(f,"JPEG",quality=85)
		except Exception as e:
			print(f"Error - Could not save image no. {i} of {name}")
			continue
	return

Driver_path = "/home/ankit/chromedriver"
to_find = list(map(str,input().split()))
howmany = int(input())
wd = webdriver.Chrome(executable_path=Driver_path)
image_scraper(wd,to_find,howmany)