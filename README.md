
# freefire-like-tool

# FF Like API Library (ff_like_api) 🚀

`ff_like_api` एक कस्टम पाइथन लाइब्रेरी है जिसकी मदद से आप बहुत ही आसानी से अपनी खुद की Free Fire Like API सर्विस चालू कर सकते हैं।

इस लाइब्रेरी की सबसे बड़ी खासियत यह है कि इसमें **आपको अपने निजी JWT टोकन्स (Tokens) लाइब्रेरी के अंदर देने की जरूरत नहीं है।** लाइब्रेरी आपके लोकल फ़ोल्डर (Current Working Directory) से `token_ind.json` या अन्य टोकन फ़ाइलों को खुद ब खुद लोड कर लेती है।

---

## 📌 फ़ीचर्स (Features)

* **Easy Setup:** सिर्फ 3-4 लाइन के कोड से Flask API चालू हो जाती है।
* **User-Owned Tokens:** यूजर अपनी खुद की टोकन फ़ाइल्स (`token_ind.json`, `token_br.json`, आदि) का इस्तेमाल कर सकता है।
* **Multi-Region Support:** IND, BR, US, SAC, NA और BD रीजन्स के लिए ऑटोमैटिक यूआरएल (URL) और टोकन राउटिंग।
* **Custom API Keys:** आप अपनी मनपसंद API Key सेट कर सकते हैं।
* **Daily Limit & Tracker:** एपीआई में डेली लिमिट और यूसेज ट्रैकर (`/remain` एंडपॉइंट) पहले से इनबिल्ट है।

---

## 📥 इंस्टॉलेशन (Installation)

अपने Termux या Terminal में नीचे दी गई कमांड चलाकर लाइब्रेरी इंस्टॉल करें:

```bash
pip install git+[https://github.com/YOUR_GITHUB_USERNAME/ff_like_api.git](https://github.com/YOUR_GITHUB_USERNAME/ff_like_api.git)
