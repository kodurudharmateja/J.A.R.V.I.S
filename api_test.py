from google import genai

client = genai.Client(api_key="AIzaSyCebrn1Q1y23bp9txFT76GW90QvYAtgkcU")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Hello"
)

print(response.text)