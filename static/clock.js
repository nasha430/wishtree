const clock = document.querySelector('h2#clock');
// const weatherIcon = document.querySelector('#weather img');


function getClock() {
    const date = new Date();
    // clock.innerText = (`${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`)
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    // const seconds = String(date.getSeconds()).padStart(2,'0');
    const hoursW = date.getHours();
    // const minutesW = date.getMinutes();

    clock.innerText = `${hours}:${minutes}`

}
//     // 날씨 이미지 가져오기
//     if(0<=hoursW<=7) {
//        weatherIcon.src = `https://mail.google.com/mail/u/0?ui=2&ik=fb199c86c4&attid=0.2&permmsgid=msg-f:1749710968493575643&th=184838db00aa0ddb&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ96KrK7aop9Fjae2r1n8luAVeqDKk-CaJBmhEbaQQQ8FjHZnzmIvZtkRvzG69rWRV5ylGrj9pe2L6quREEAb2cO4ccciY0f-Kn9hEfDCNyekgqQpBTRCbPKayk&disp=emb&realattid=ii_lakhqg7m2`;
//     }else if(8<=hours<=12) {
//         weatherIcon.src = `https://mail.google.com/mail/u/0?ui=2&ik=fb199c86c4&attid=0.4&permmsgid=msg-f:1749710968493575643&th=184838db00aa0ddb&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ9Wn-kXUcpnymOPlgIRpbK2l5W-EwX4CCFVUZ6ik1kZgLXDCWHvZUO5gq_XY5-lgHkyMDYsY6ndVZOHGz9zcYUrtOLmF9w6M_b27aHI7S5f4Mw75JqmeekqM1Y&disp=emb&realattid=ii_lakhqg7s4`;
//     }else if(12<=hours<=18) {
//         weatherIcon.src = `https://mail.google.com/mail/u/0?ui=2&ik=fb199c86c4&attid=0.1&permmsgid=msg-f:1749710968493575643&th=184838db00aa0ddb&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ9u-AKdyFCDfEq30jcSF_8PIKnHB9Cxdqzz7b-nASVe0UP9PW4pNRsnfMwUgtb3favwdj-cJmEqRf0PhrcnCruDAz3y2GmUccnr1PDy4Lm38NNxIM8A0OvDhis&disp=emb&realattid=ii_lakhqg7p3`;
//     }else {
//         weatherIcon.src = `https://mail.google.com/mail/u/0?ui=2&ik=fb199c86c4&attid=0.6&permmsgid=msg-f:1749710968493575643&th=184838db00aa0ddb&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ8kxc0oaLDyoBhYTT6N-ZPqpB8R9hlZVm12PiZZMB9EXNZ5LR7_yxtmrzzfgSOqpiYUolsEJu5_Dlz1mwe_M9kkPxGkgbt8Rk_b76MdQQNYBcyHlftiMC183Ck&disp=emb&realattid=ii_lakhqg7v5`;
//     }
// }

getClock(); //1초뒤가 아닌 page를 열면 바로 시작될 수 있도록. 
setInterval(getClock,60000);





