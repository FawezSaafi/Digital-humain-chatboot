import wolframalpha
import webbrowser
# Taking input from user
def search(question):
   question = input('Question: ')

   # App id obtained by the above steps
   app_id = "K9T3H2-57578YL87T"
   # Instance of wolf ram alpha
   # client class
   try:
      client = wolframalpha.Client(app_id)

      # Stores the response fromtemperature of the sun
      # wolf ram alpha
      res = client.query(question)
    # Includes only text from the response
      answer = next(res.results).text

   except:
       line = 'http://api.wolframalpha.com/v1/simple?appid=VKY3JH-44A8L5PK3X&i=%3F'

       index = line.find('%3F')
       output_line = line[:index] + question + line[index:]
       webbrowser.open(output_line)
   print(answer)

