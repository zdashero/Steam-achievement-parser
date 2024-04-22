# Steam Achievement Parser

This script allows you to retrieve achievement data from the Steam API, download associated images, and process the data into a JSON file. (JSON IS ALSO GOLDBERG READY)

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Requests library (can be installed via `pip install requests`)

## Usage

1. Replace `CHANGE ME` with your Steam WebAPI key in the script. (on line 11 in main.py)
2. Run the script with the following command: "python main.py <appid>
3. Replace `<appid>` with the Steam App ID of the game you want to retrieve achievement data for.

## Steps to Get a WebAPI Key

1. **Sign in to Steam**: If you haven't already, sign in to your Steam account.

2. **Go to Steamworks Developer Site**: Visit the [Steamworks Developer Site](https://steamcommunity.com/dev/apikey).

3. **Fill out the Form**: You'll see a form titled "Get a Steam Web API Key". In the "Domain" field, you can enter your domain name if you have one, or you can leave it blank.

4. **Accept the Terms**: Read and accept the Steam Subscriber Agreement by checking the box.

5. **Submit**: Click on the "I agree, submit" button.

6. **Get Your Key**: After submitting the form, your WebAPI key will be generated. Copy this key.

7. **Update Script**: Replace `CHANGE ME` in the script with your newly generated key.


## File Structure

- `main.py`: Main script file.
- `images/`: Folder to store downloaded images.
- `achievements.json`: JSON file containing processed achievement data.

## License

This project is licensed under the GNU GPLV3 License. See the [LICENSE](LICENSE) file for details.

