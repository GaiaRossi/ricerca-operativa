# PSEUDOCODICE
Da decidere:
- che ordine ogni paziente fa i test
- in che posizione si trova rispetto agli altri pazienti che entrano nella stessa saletta
- in che saletta entra il paziente (questa per ultima perché più probabile che renda non ammissibile)

Tralasciando l'ordine di esecuzione dei test del singolo paziente, posso decidere in che
saletta mettere il paziente basandomi sulla somma dei tempi dei suoi test e cercare di minimizzare (non guardo
gli operatori), rendendono essenzialmente un problema job shop dove le sale sono le macchine.
Una volta però deciso come ordinarli, devo capire in che ordine mettere gli operatori e decidere
il percorso degli operatori comporta anche decidere l'ordine di esecuzione dei test del paziente.
Fissata quindi la sala e l'ordine, cerco un cammino per gli operatori che non generi cicli e non generi ritardi.