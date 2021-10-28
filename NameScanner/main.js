const axios = require('axios');
const fs = require('fs');

const startString = '<div class="name t-colour">';

process.on('uncaughtException', (e) => console.error(e));
process.on('unhandledRejection', (e) => console.error(e));

const main = async () => {

    let offset = 0;
    while (offset < 100000) {
        const ids = [...Array(10).keys()].map(i => i + offset);
        const promises = ids.map(id => axios.get(`https://www.premierleague.com/players/${id}`));
        const responses = await Promise.allSettled(promises);
        responses.forEach((res, i) => {
            try {
                if (res.value.data.includes('<div class="name t-colour">')) {
                    const startPos = res.value.data.indexOf(startString);
                    const match = res.value.data.substring(startPos + startString.length, res.value.data.indexOf('</div>', startPos));
                    console.log(i);
                    fs.appendFileSync('./temp.txt', `${i + offset}: ${match}\n`);
                }
                else {
                    console.error("Weird Flex but ok");
                }
            }
            catch (e) {
                console.error(`Exception`);
            }
        });
        offset += 10;
        console.log(`Fetched ${offset}`);
    }
};

main();