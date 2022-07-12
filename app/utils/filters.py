def format_date(date):
  return date.strftime('%m/%d/%y')

def format_url(url): # url: string
  return (
    url # remove all parts of url that aren't the domain name
      .replace('http://', '')
      .replace('https://', '')
      .replace('www.', '')
      .split('/')[0]
      .split('?')[0]
  )

def format_plural(amount, word):
  if amount !=1:
    return word + 's'
  
  return word
