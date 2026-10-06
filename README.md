<div align="center">

<h3><code>eduardoruisjbv@github ~ $ ./contributions --year</code></h3>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./contrib-heatmap.svg">
  <source media="(prefers-color-scheme: light)" srcset="./contrib-heatmap-light.svg">
  <img src="./contrib-heatmap-light.svg" width="860" alt="Eduardoruisjbv's GitHub contribution calendar" />
</picture>

<br><br>

<h3><code>eduardoruisjbv@github ~ $ whoami</code></h3>

<table>
  <tr>
    <td valign="top"><picture><source media="(prefers-color-scheme: dark)" srcset="./avatar-ascii.svg"><source media="(prefers-color-scheme: light)" srcset="./avatar-ascii-light.svg"><img src="./avatar-ascii-light.svg" width="420" alt="Rui's profile avatar rendered as animated ASCII art" /></picture></td>
    <td valign="top"><picture><source media="(prefers-color-scheme: dark)" srcset="./rui-profile-card.svg"><source media="(prefers-color-scheme: light)" srcset="./rui-profile-card-light.svg"><img src="./rui-profile-card-light.svg" width="420" alt="Rui's profile and focus" /></picture></td>
  </tr>
</table>

<br>

<p><b>AI Systems &amp; Product Engineer</b></p>

[![Portfolio](https://img.shields.io/badge/Portfolio-eduardorui.com.br-0d1117?style=for-the-badge&logo=vercel&logoColor=white)](https://eduardorui.com.br/)
[![GitHub](https://img.shields.io/badge/GitHub-eduardoruisjbv-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/eduardoruisjbv)

</div>

## Refresh the profile art

The contribution graph updates daily through GitHub Actions. To regenerate the avatar art after changing `source-photo.jpg`, install the dependencies and run:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/prep_photo.py
python scripts/make_ascii_svg.py
PROFILE_THEME=light python scripts/make_ascii_svg.py
python scripts/make_info_card.py
PROFILE_THEME=light python scripts/make_info_card.py
```

The daily job only needs the public GitHub contributions page; it uses no personal access token.
