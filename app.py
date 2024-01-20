from flask import Flask, render_template, request
import predictPhish
import sql
import firewallRule

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('phishing.html')


@app.route('/phishing', methods=['GET', 'POST'])
def url():
    url_requested = ['']
    if request.method == 'GET':
        url_requested = request.args.get('url')
        y_pred, y_phishing, y_non_phishing = predictPhish.phishPrediction(url_requested)
        if y_phishing >= 0.5:
            sql.phishing(url_requested)
            domain = firewallRule.getDomain(url_requested)
            BLOCK = f"127.0.0.1 {domain}"
            firewallRule.BlockURL(BLOCK)
        return render_template('phishing.html', phish=y_phishing, non_phish=y_non_phishing,
                               url=url_requested)  # type: ignore
    return render_template('phishing.html', phish=0, non_phish=0, url=url_requested)

@app.route('/deleteurl')
def deleteurl():
    sno = []
    url = []
    urls = sql.getPhishURLS()
    for i in enumerate(urls):
        sno.append(i[0])
        url.append(i[1][0])
    return render_template('iptables.html', snos=sno, urls=url)

@app.route('/phishing-new')
def phishingnew():
    if request.method == 'GET':
        number = request.args.get('number')
        sno = []
        url = []
        urls = sql.getPhishURLS()
        for i in enumerate(urls):
            sno.append(i[0])
            url.append(i[1])
        phishingURL_to_delete = url[int(number)]
        print(phishingURL_to_delete)
        domain = firewallRule.getDomain(phishingURL_to_delete[0])
        print(domain)
        BLOCK = f"127.0.0.1 {domain}"
        firewallRule.deleteBlockedURL(BLOCK)

    return render_template('phishing.html')

app.run(host='0.0.0.0', port=7777)
