import requests

url = "https://www.cnp.fr/cnp/content/download/11474/file/CNP-Assurances-Bilan-social-2023.pdf"
response = requests.get(url)

if response.status_code == 200:
    with open("bilan-social.pdf", "wb") as file:
        file.write(response.content)
    print("Téléchargement réussi.")
else:
    print("Échec du téléchargement :", response.status_code)
