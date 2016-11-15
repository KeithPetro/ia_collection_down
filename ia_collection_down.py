#Internet Archive Collection Downloader
#2016/11/15
#Usage: ia_collection_down.py [Collection Name]

import internetarchive as ia
import sys
import time

#Error log
error_log = open('ia_errors.log', 'a')

#If number of args is wrong, print usage
if(len(sys.argv) != 2):
	print("Usage:")
	print("	ia_collection_down.py [Collection Name]")
	sys.exit()

collection = sys.argv[1]
collection_results = ia.search_items('collection:' + collection)

#Exit if no collection items found
if(len(collection_results) == 0):
	print("No collection " + collection)
	sys.exit()

total_count = len(collection_results)

current_item = 1
for i in collection_results:
	item_id = i['identifier']
	
	item = ia.get_item(item_id)

	#Download all files in the item, log any exceptions
	try:
		item.download(verbose=True)
	except Exception as e:
		error_log.write(item_id + ": Download failed due to error - %s\n" % e)
		print("ERROR on downloading " + item_id)
	else:
		print("Downloading item " + str(current_item) + "/" + str(total_count) + " " + item_id + '...')
		time.sleep(1)

	#Show percentage every 10 entries
	if(current_item % 10 == 0):
		print(str(current_item / total_count * 100) + "% of items completed")

	current_item += 1
