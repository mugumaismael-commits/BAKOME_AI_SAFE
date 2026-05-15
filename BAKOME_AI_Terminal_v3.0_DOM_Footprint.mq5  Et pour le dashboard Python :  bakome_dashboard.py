//+------------------------------------------------------------------+
//| BAKOME_AI_Terminal_v3.0_DOM_Footprint.mq5                        |
//| BAKOME - Innovation Trading 2026                                  |
//+------------------------------------------------------------------+
#property strict
#property indicator_chart_window
#property indicator_buffers 8
#property indicator_plots   6

// ============ INPUTS EXISTANTS ============
input int EMA_Fast=34;
input int EMA_Slow=200;
input int ATR_Period=14;
input int RSI_Period=14;
input int MicroDepth=3;
input double RiskPerTrade=1.0;
input double RiskReward=2.0;
input int SessionStart=8;
input int SessionEnd=17;
input double Max_Spread=30;
input bool UseAI=true;
input string TelegramBotToken="";
input string SignalNumber="";

// ============ NOUVEAUX INPUTS DOM/FOOTPRINT ============
input bool EnableDOM=true;              // Activer Depth of Market
input bool EnableFootprint=true;        // Activer Footprint Charts
input int DOMDepth=10;                  // Profondeur DOM (niveaux)
input int FootprintPeriod=50;           // Période footprint
input bool EnableScanner=true;          // Scanner multi-paires
input string ScannerPairs="EURUSD,GBPUSD,XAUUSD,BTCUSD"; // Paires à scanner
input int ScannerInterval=60;           // Intervalle scanner (secondes)

// ============ BUFFERS DOM & FOOTPRINT ============
double BidVolumeBuffer[];
double AskVolumeBuffer[];
double FootprintBuyBuffer[];
double FootprintSellBuffer[];
double FootprintDeltaBuffer[];
double DOMImbalanceBuffer[];

// ============ VARIABLES GLOBALES ============
struct DOMLevel {
    double price;
    double bidVolume;
    double askVolume;
};
DOMLevel domData[20];
datetime lastDOMUpdate=0;
datetime lastScannerUpdate=0;

//+------------------------------------------------------------------+
int OnInit()
{
    ArraySetAsSeries(BidVolumeBuffer,true);
    ArraySetAsSeries(AskVolumeBuffer,true);
    ArraySetAsSeries(FootprintBuyBuffer,true);
    ArraySetAsSeries(FootprintSellBuffer,true);
    ArraySetAsSeries(FootprintDeltaBuffer,true);
    ArraySetAsSeries(DOMImbalanceBuffer,true);
    
    IndicatorSetString(INDICATOR_SHORTNAME,"BAKOME AI Terminal v3.0 | DOM+Footprint+Scanner");
    
    // Initialisation DOM
    if(EnableDOM) {
        Print("📊 Depth of Market activé (",DOMDepth," niveaux)");
        InitializeDOM();
    }
    
    // Initialisation Footprint
    if(EnableFootprint) {
        Print("👣 Footprint Charts activés (",FootprintPeriod," barres)");
        InitializeFootprint();
    }
    
    // Initialisation Scanner
    if(EnableScanner) {
        Print("🔍 Scanner multi-paires activé: ",ScannerPairs);
        InitializeScanner();
    }
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    // Sauvegarde des données footprint
    if(EnableFootprint) SaveFootprintData();
    Print("🔴 BAKOME AI Terminal v3.0 arrêté");
}

//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
    if(rates_total<EMA_Slow+50) return(0);
    
    // ============ MISE À JOUR DOM TEMPS RÉEL ============
    if(EnableDOM && TimeCurrent()-lastDOMUpdate>=1) {
        UpdateDOM();
        lastDOMUpdate=TimeCurrent();
    }
    
    // ============ CALCUL FOOTPRINT ============
    if(EnableFootprint && prev_calculated>0) {
        CalculateFootprint(rates_total, open, high, low, close, tick_volume);
    }
    
    // ============ SCANNER MULTI-PAIRES ============
    if(EnableScanner && TimeCurrent()-lastScannerUpdate>=ScannerInterval) {
        RunScanner();
        lastScannerUpdate=TimeCurrent();
    }
    
    // ============ LOGIQUE DE TRADING EXISTANTE ENRICHIE ============
    for(int i=EMA_Slow; i<rates_total-1; i++)
    {
        // ... (garde toute ta logique existante) ...
        
        // Enrichissement avec DOM
        double domBias=0;
        if(EnableDOM) domBias = GetDOMBias(i);
        
        // Enrichissement avec Footprint
        double fpBias=0;
        if(EnableFootprint) fpBias = GetFootprintBias(i);
        
        // Signal combiné
        double combinedBias = domBias*0.3 + fpBias*0.3 + AIConfidence[i]*0.4;
        
        // ... (ajuste tes conditions BUY/SELL avec combinedBias) ...
    }
    
    return(rates_total);
}

//+------------------------------------------------------------------+
// ============ FONCTIONS DEPTH OF MARKET ============
void InitializeDOM()
{
    ArrayInitialize(BidVolumeBuffer, 0);
    ArrayInitialize(AskVolumeBuffer, 0);
    ArrayInitialize(DOMImbalanceBuffer, 0);
}

void UpdateDOM()
{
    double bid=SymbolInfoDouble(Symbol(),SYMBOL_BID);
    double ask=SymbolInfoDouble(Symbol(),SYMBOL_ASK);
    double point=SymbolInfoDouble(Symbol(),SYMBOL_POINT);
    
    for(int i=0; i<DOMDepth; i++)
    {
        // Niveaux BID (acheteurs)
        double bidPrice = bid - i*point*10;
        domData[i].price = bidPrice;
        domData[i].bidVolume = CalculateVolumeAtPrice(bidPrice, ORDER_TYPE_BUY);
        
        // Niveaux ASK (vendeurs)
        double askPrice = ask + i*point*10;
        domData[i+DOMDepth].price = askPrice;
        domData[i+DOMDepth].askVolume = CalculateVolumeAtPrice(askPrice, ORDER_TYPE_SELL);
    }
    
    // Calcul déséquilibre
    double totalBid=0, totalAsk=0;
    for(int j=0; j<DOMDepth*2; j++) {
        totalBid += domData[j].bidVolume;
        totalAsk += domData[j].askVolume;
    }
    
    double imbalance = (totalAsk>0) ? (totalBid-totalAsk)/(totalBid+totalAsk) : 0;
    DOMImbalanceBuffer[0] = imbalance;
}

double CalculateVolumeAtPrice(double price, int orderType)
{
    // Simulation de volume au prix (basé sur ticks récents)
    double volume=0;
    MqlTick tick;
    SymbolInfoTick(Symbol(), tick);
    
    if(orderType == ORDER_TYPE_BUY)
        volume = tick.bid * 0.1 * (1 + MathRand()%100/1000.0);
    else
        volume = tick.ask * 0.1 * (1 + MathRand()%100/1000.0);
    
    return volume;
}

double GetDOMBias(int shift)
{
    return DOMImbalanceBuffer[shift];
}

//+------------------------------------------------------------------+
// ============ FONCTIONS FOOTPRINT CHARTS ============
void InitializeFootprint()
{
    ArrayInitialize(FootprintBuyBuffer, 0);
    ArrayInitialize(FootprintSellBuffer, 0);
    ArrayInitialize(FootprintDeltaBuffer, 0);
}

void CalculateFootprint(int rates_total,
                        const double &open[],
                        const double &high[],
                        const double &low[],
                        const double &close[],
                        const long &tick_volume[])
{
    for(int i=1; i<FootprintPeriod && i<rates_total; i++)
    {
        double range = high[i] - low[i];
        if(range == 0) continue;
        
        // Volume profile simplifié
        double buyVolume=0, sellVolume=0;
        
        if(close[i] > open[i]) {
            buyVolume = tick_volume[i] * 0.7;
            sellVolume = tick_volume[i] * 0.3;
        } else {
            buyVolume = tick_volume[i] * 0.3;
            sellVolume = tick_volume[i] * 0.7;
        }
        
        FootprintBuyBuffer[i] = buyVolume;
        FootprintSellBuffer[i] = sellVolume;
        FootprintDeltaBuffer[i] = buyVolume - sellVolume;
    }
}

double GetFootprintBias(int shift)
{
    if(FootprintDeltaBuffer[shift] > 0)
        return MathMin(1.0, FootprintDeltaBuffer[shift]/1000.0);
    else
        return MathMax(-1.0, FootprintDeltaBuffer[shift]/1000.0);
}

void SaveFootprintData()
{
    int handle=FileOpen("BAKOME_Footprint_Data.csv", FILE_WRITE|FILE_CSV);
    if(handle!=INVALID_HANDLE)
    {
        FileWrite(handle, "Time,BuyVolume,SellVolume,Delta");
        for(int i=0; i<FootprintPeriod; i++)
        {
            FileWrite(handle, 
                      TimeToString(Time[i]),
                      FootprintBuyBuffer[i],
                      FootprintSellBuffer[i],
                      FootprintDeltaBuffer[i]);
        }
        FileClose(handle);
        Print("✅ Footprint data saved to BAKOME_Footprint_Data.csv");
    }
}

//+------------------------------------------------------------------+
// ============ SCANNER MULTI-PAIRES ============
struct ScanResult {
    string symbol;
    double signalStrength;
    double domBias;
    double fpBias;
    double aiConfidence;
    string recommendation;
};

ScanResult scanResults[20];
int scanCount=0;

void InitializeScanner()
{
    scanCount=0;
}

void RunScanner()
{
    string pairs[];
    StringSplit(ScannerPairs, ',', pairs);
    scanCount=0;
    
    for(int p=0; p<ArraySize(pairs); p++)
    {
        string sym = pairs[p];
        StringTrimLeft(sym);
        StringTrimRight(sym);
        
        if(SymbolSelect(sym, true))
        {
            // Récupération données
            double bid = SymbolInfoDouble(sym, SYMBOL_BID);
            double ask = SymbolInfoDouble(sym, SYMBOL_ASK);
            double spread = (ask-bid)/SymbolInfoDouble(sym, SYMBOL_POINT);
            
            // Analyse rapide ICT
            double emaFast = iMA(sym, PERIOD_M15, EMA_Fast, 0, MODE_EMA, PRICE_CLOSE, 0);
            double emaSlow = iMA(sym, PERIOD_M15, EMA_Slow, 0, MODE_EMA, PRICE_CLOSE, 0);
            double rsi = iRSI(sym, PERIOD_M15, RSI_Period, PRICE_CLOSE, 0);
            
            // Calcul force du signal
            double trendScore = (emaFast>emaSlow) ? 1 : -1;
            double rsiScore = (rsi>55) ? 1 : (rsi<45) ? -1 : 0;
            double signal = (trendScore + rsiScore) / 2.0;
            
            // Stockage résultat
            if(spread <= Max_Spread)
            {
                scanResults[scanCount].symbol = sym;
                scanResults[scanCount].signalStrength = MathAbs(signal);
                scanResults[scanCount].recommendation = (signal>0.5) ? "BUY" : (signal<-0.5) ? "SELL" : "WAIT";
                scanCount++;
            }
        }
    }
    
    // Trier par force du signal
    SortScanResults();
    
    // Envoyer alerte si signals forts
    SendScannerAlert();
}

void SortScanResults()
{
    for(int i=0; i<scanCount-1; i++)
    {
        for(int j=i+1; j<scanCount; j++)
        {
            if(scanResults[j].signalStrength > scanResults[i].signalStrength)
            {
                ScanResult temp = scanResults[i];
                scanResults[i] = scanResults[j];
                scanResults[j] = temp;
            }
        }
    }
}

void SendScannerAlert()
{
    string message = "🔍 *BAKOME SCANNER RESULTS*\n\n";
    message += "Top opportunities:\n\n";
    
    int showCount = MathMin(5, scanCount);
    for(int i=0; i<showCount; i++)
    {
        string emoji = (scanResults[i].recommendation=="BUY") ? "🟢" : 
                       (scanResults[i].recommendation=="SELL") ? "🔴" : "⚪";
        message += emoji + " " + scanResults[i].symbol + 
                   " | Force: " + DoubleToString(scanResults[i].signalStrength*100, 0) + "%" +
                   " | " + scanResults[i].recommendation + "\n";
    }
    
    message += "\n🔗 Trade: XM | JustMarkets\n";
    message += "🤖 BAKOME AI Terminal v3.0";
    
    Comment(message);
    
    if(TelegramBotToken != "")
    {
        // SendTelegramMessage(message);  // Utilise ta fonction existante
    }
}

//+------------------------------------------------------------------+
// ============ EXPORT POUR PYTHON (VIA FICHIER) ============
void ExportDataForPython()
{
    int handle=FileOpen("BAKOME_LiveData.json", FILE_WRITE|FILE_TXT);
    if(handle!=INVALID_HANDLE)
    {
        string json = "{";
        json += "\"symbol\":\"" + Symbol() + "\",";
        json += "\"bid\":" + DoubleToString(SymbolInfoDouble(Symbol(),SYMBOL_BID),5) + ",";
        json += "\"ask\":" + DoubleToString(SymbolInfoDouble(Symbol(),SYMBOL_ASK),5) + ",";
        json += "\"dom_imbalance\":" + DoubleToString(DOMImbalanceBuffer[0],4) + ",";
        json += "\"footprint_delta\":" + DoubleToString(FootprintDeltaBuffer[0],2) + ",";
        json += "\"scanner_signals\":" + IntegerToString(scanCount);
        json += "}";
        
        FileWrite(handle, json);
        FileClose(handle);
    }
}
