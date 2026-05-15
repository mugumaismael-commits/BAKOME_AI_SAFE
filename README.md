
<p align="center">
  <img src="https://via.placeholder.com/800x400/0a0a0a/00ff88?text=BAKOME+AI+Terminal+v3.0+DOM+Footprint+Scanner" alt="BAKOME AI Terminal" width="100%">
</p>

---

## 📖 Description

**🇫🇷 Français**
BAKOME AI Terminal v3.0 est un Expert Advisor MQL5 nouvelle génération pour XAUUSD. Il combine 5 couches d'analyse (SuperTrend, filtre de Kalman, RSI, Vertex microstructure, IA neuronale tanh) avec trois innovations majeures : **Depth of Market** en temps réel (déséquilibre acheteurs/vendeurs), **Footprint Charts** (delta volume par prix), et un **scanner multi-paires** automatisé. Un dashboard web Python affiche tout en direct pour attirer sponsors et investisseurs. Développé intégralement sur un Pixel 4a 5G à Goma, RDC.

**🇬🇧 English**
BAKOME AI Terminal v3.0 is a next-generation MQL5 Expert Advisor for XAUUSD. It combines 5 analytical layers (SuperTrend, Kalman filter, RSI, Vertex microstructure, tanh neural AI) with three major innovations: real-time **Depth of Market** (buyer/seller imbalance), **Footprint Charts** (volume delta by price), and an automated **multi-pair scanner**. A Python web dashboard displays everything live to attract sponsors and investors. Built entirely on a Pixel 4a 5G in Goma, DRC.

**🇪🇸 Español**
BAKOME AI Terminal v3.0 es un Expert Advisor MQL5 de nueva generación para XAUUSD. Combina 5 capas de análisis (SuperTrend, filtro Kalman, RSI, Vertex microestructura, IA neuronal tanh) con tres innovaciones principales: **Depth of Market** en tiempo real (desequilibrio comprador/vendedor), **Footprint Charts** (delta de volumen por precio), y un **escáner multi-pares** automatizado. Un dashboard web Python muestra todo en directo para atraer patrocinadores e inversores. Desarrollado íntegramente en un Pixel 4a 5G en Goma, RDC.

---

## ⚡ Features / Fonctionnalités / Características

- 🧠 **Neural AI** (tanh) + ICT + Kalman filter + SuperTrend + RSI
- 📊 **Depth of Market** — déséquilibre acheteurs/vendeurs en temps réel
- 👣 **Footprint Charts** — delta volume, volume profile par prix
- 🔍 **Scanner multi-paires** — ICT + RSI + tendance sur 28 paires
- 💻 **Dashboard web Python** — interface live pour sponsors
- 📡 **Alertes Telegram & Signal** avec liens brokers intégrés
- ⚙️ **Risk management dynamique** (ATR + confiance IA)
- 🔗 **Liens XM Global & JustMarkets** dans chaque notification

---

## ⚙️ Quick Install / Installation rapide / Instalación rápida

1. Copier `BAKOME_AI_Terminal_v3.0_DOM_Footprint.mq5` dans le dossier `Experts` ou `Indicators` de MT5
2. Compiler dans MetaEditor
3. Attacher sur un graphique **XAUUSD** (M5 ou M15 recommandé)
4. Configurer le token Telegram et/ou le numéro Signal (optionnel)
5. Lancer `bakome_dashboard.py` pour le dashboard web :
   ```bash
   pip install flask
   python bakome_dashboard.py
