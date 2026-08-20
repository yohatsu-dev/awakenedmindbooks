const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const startStr = '<section class="email-section" id="novidades">';
const start = html.indexOf(startStr);
const endStr = '</section>';
const end = html.indexOf(endStr, start) + endStr.length;

if (start !== -1 && end !== -1) {
  const newSection = `<section class="email-section" id="novidades">
    <div class="container">
      <div class="email-card email-card--promo fade-in" style="display: grid; grid-template-columns: 1fr 2fr; gap: 40px; align-items: center; text-align: left;">
        <div class="promo-image">
          <img src="assets/covers/kshitigarbha-pt.png" alt="Capa do E-book Kshitigarbha, edição gratuita" style="width: 100%; border-radius: 4px; box-shadow: 0 12px 24px rgba(0,0,0,0.2);">
        </div>
        <div class="promo-content">
          <div class="badge badge--ku" style="margin-bottom: 20px; display: inline-block;">
            <span data-lang="pt">EDIÇÃO GRATUITA EXCLUSIVA</span>
            <span data-lang="en">EXCLUSIVE FREE EDITION</span>
          </div>
          <h2 class="email-title" style="text-align: left; margin-bottom: 15px;">
            <span data-lang="pt">Existe uma dor que o tempo não cura. Mas ela pode ser desinstalada.</span>
            <span data-lang="en">There is a pain that time does not heal. But it can be uninstalled.</span>
          </h2>
          <p class="email-subtitle" data-lang="pt" style="text-align: left; opacity: 0.9; margin-bottom: 25px;">Ninguém te dá licença para sofrer a perda de alguém que foi embora. Disseram que você precisa ser forte e "superar". É mentira.<br><br><strong>Kshitigarbha</strong> é o próximo livro da série. Ele revela o método tibetano direto e sem enrolação para atravessar o luto, aceitar o fim e rodar o sistema com a perda dentro dele, sem travar. <b>Assine a newsletter agora e receba o PDF com o capítulo completo na mesma hora, grátis.</b></p>
          <p class="email-subtitle hidden" data-lang="en" style="text-align: left; opacity: 0.9; margin-bottom: 25px;">No one gives you permission to grieve the loss of someone who left. They told you to be strong and "move on." That's a lie.<br><br><strong>Kshitigarbha</strong> is the next book in the series. It reveals the direct, no-nonsense Tibetan method for moving through grief, accepting the end, and running the system with loss inside it, without freezing. <b>Subscribe to the newsletter now and get the full chapter PDF instantly, for free.</b></p>
          
          <form class="email-form" id="newsletter-form" action="https://mentedespertabooks.substack.com/api/v1/free?nojs=true" method="POST" target="_blank">
            <div class="email-form-row">
              <label for="email-input" class="sr-only"><span data-lang="pt">Seu e-mail</span><span data-lang="en">Your email</span></label>
              <input type="email" id="email-input" name="email" class="email-input" placeholder="seu@email.com" data-pt-placeholder="seu@email.com" data-en-placeholder="your@email.com" required>
              <button type="submit" class="cta-btn cta-btn--primary email-submit">
                <span data-lang="pt">Quero meu Livro Grátis</span>
                <span data-lang="en">Get My Free Book</span>
              </button>
            </div>
            <p class="email-note" data-lang="pt" style="font-size: 0.8rem; margin-top: 15px; opacity: 0.6;">Você será redirecionado ao Substack. O link do PDF chegará no primeiro e-mail de boas-vindas.</p>
            <p class="email-note hidden" data-lang="en" style="font-size: 0.8rem; margin-top: 15px; opacity: 0.6;">You will be redirected to Substack. The PDF link will arrive in your welcome email.</p>
          </form>
        </div>
      </div>
    </div>
  </section>`;

  html = html.substring(0, start) + newSection + html.substring(end);
  fs.writeFileSync('index.html', html, 'utf8');
  console.log('Update successful.');
} else {
  console.log('Section not found.');
}
