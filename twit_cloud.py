import tweepy, configparser, wordcloud, re, sys
import multidict as multidict

def create_api():
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_secret = config['twitter']['api_secret']
    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    auth = tweepy.OAuth1UserHandler(
      api_key, api_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    return api

def extract_text(userID):
    tweets = create_api().user_timeline(screen_name=userID, 
                              # 200 is the maximum allowed count
                              count=200,
                              include_rts = False,
                              # Necessary to keep full_text 
                              # otherwise only the first 140 words are extracted
                              tweet_mode = 'extended'
                              )


    text_list= [info.full_text for info in tweets]
    filtered_text = [re.sub('@\S+', '', i) for i in text_list]
    filtered_text2 = [re.sub('https\S+', '', i) for i in filtered_text]
    text = " ".join(filtered_text2).split(" ")

    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    for t in text:
        val = tmpDict.get(t, 0)
        tmpDict[t.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

def main():
    args = sys.argv[1]
    _wordcloud = wordcloud.WordCloud(min_word_length=4, background_color="white").generate_from_frequencies(extract_text(args),)
    image = _wordcloud.to_image()
    image.show()



if __name__ == '__main__':
    main()
