chrome.downloads.onCreated.addListener(function(downloadItem){
    document.title = downloadItem.url;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
  chrome.tabs.sendMessage(tabs[0].id, {itemurl: downloadItem.url}, function(response){
   console.log(response.farewell)
  });
 });
});