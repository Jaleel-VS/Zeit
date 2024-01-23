# Zeit

Zeit is a simple course scheduler for the Udemy platform. It takes input from a user and returns a daily schedule of which lectures on which day.

For now it's a command line application, but I plan to make it a web app in the future.

## Installation

Clone the repository and make a virtual environment. Then install the requirements from the `requirements.txt` file.

```bash
git clone <repo url>
cd zeit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

(Windows users can use `venv\Scripts\activate` instead of `source venv/bin/activate`)

## Usage

Run the `zeit.py` file with Python 3.6 or higher. You will be prompted to enter the URL of the course you want to schedule.

```bash
python3 zeit.py
```

### Screenshots

![Screenshot 1](https://media.discordapp.net/attachments/808679873837137940/1196159083405910138/image.png?ex=65b69cf5&is=65a427f5&hm=c526e51390400792f70aacc4bf48a5e1981f7b16d897dd22e29dac00b5a99e8b&=&format=webp&quality=lossless "user input")

![Screenshot 2](https://media.discordapp.net/attachments/702400926270488601/1196164033334751232/image.png?ex=65b6a191&is=65a42c91&hm=1d31aeb5dce9ff59d50d56c79dea5c1df3553971364eec90d3e131fe69877f45&=&format=webp&quality=lossless&width=482&height=403 "ouput")

Follow the prompts, after which you will be presented with a daily schedule of lectures that is saved to a file called `<id>_schedule.txt`.

## Future Plans

- [ ] Make a web app
- [ ] Reorganize code into modules
- [ ] Write unit tests
- [ ] Add support for other platforms (Coursera, Youtube, LinkedInLearning edX, etc.)
- [ ] Add support for other date formats
