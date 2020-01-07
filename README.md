# Autogram
A automated Instagram poster.

## Why?
I am fed up of keeping track of my Instagram posts and when I should schedule them. Therefore, I created `Autogram`.
A automated way of uploading to Instagram.

> Note: InstagramAPI did not work when building this for posting photos. So I had to build a workaround.

## How to use
1. Add __Instagram ready images__ to the [`/posts`](posts) directory. These are common image file types (`.jpeg`, `.png`, etc...)
and also 1:1 square images. So `1080px x 1080px` images.

2. Download and install [chromedriver](https://chromedriver.chromium.org/) for your version of Chrome. Chrome >> `...` > About Google Chrome.
Then place it in a directory [`/chromedriver`](chromedriver) as `/chromedriver/chromedriver.exe`.

3. `pip install -r requirments.txt`

4. Input your Instagram username and password in [`instagram.py`](instagram.py#L121) and run the script 
`python instagram.py` 
