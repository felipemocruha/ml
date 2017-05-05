const Nightmare = require('nightmare')
const nightmare = Nightmare({show: false})

nightmare
	.goto('https://www.submarino.com.br/produto/130918531/smartphone-samsung-galaxy-a7-dual-chip-android-6.0-tela-5.7-octa-core-1.9ghz-32gb-4g-camera-16mp-dourado')
	.wait()
	.evaluate(() => {
		window.scrollTo(0,document.body.scrollHeight)
		return document.querySelectorAll('a')
	})
	.end()
    .then(res => {
		for(i = 0; i < res.length; i++) {
			if(res[i]['href'].search('produto'))
				console.log(res[i]['href'])
		}
	})
	.catch(e => {console.log(e)})
