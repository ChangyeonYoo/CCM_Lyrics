import pandas as pd

inventors = pd.DataFrame(
    {
    'artist':['testArtist'],
    'title':['testTitle'],
    'lyrics':['testLyrics']
})
inventors = inventors.assign()
inventors.to_csv('testCSV.csv')