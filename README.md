# YpoxreotikiErgasiaSept22_E19098_Mavroeidi_Maria

Yποχρεωτική Εργασία Σεπτεμβρίου στο μάθημα Πληροφοριακά Συστήματα. 

##Περιγραφή της Εφαρμογής

Δημιουργία webservice για την υλοποίηση της υπηρεσίας DS Airlines.



##Προϋποθέσεις:

### Εγκατάσταση Docker.
 Μετά την εγκατάσταση του Docker Desktop Installer.exe Εντολή στο cmd:
`code`  pip install docker docker-compose

Tο πρόγραμμα θα εκτελείται στην πόρτα 5000 μέσω flask και η Mongodb θα βρίσκεται στην πόρτα 27017.
Στην MongoDB δημιουργήθηκε μία database "DSAirlines" με collections users και flights.

Για την δημιουργία του container, κατεβάστε αυτό το directory και εκτελέστε:
docker container create





##Web Service: Λειτουργίες Απλού Χρήστη
###/signup
Δίνοντας 0.0.0.0:5000/signup με μέθοδο POST, μπορούμε να δημιουργείτε ένας χρήστη στο σύστημα. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`code` {
        "email": "mariamavroeidi@gmail.com" ,
        "username": "mariamav",
        "fistname": "Maria",
        "lastname": "Mavroeidi",
        "password": "11111",
        "passport": "323232121",
        "category": "user"
    }
To πρόγραμμα ελέγχει έχουν αν το json αρχείο είναι στην σωστή μορφή και τότε γίνεται η δημιουργία του χρήστη.

###/login
Δίνοντας 0.0.0.0:5000/login με μέθοδο POST, μπορεί ένας χρήστης να κάνει login στο σύστημα. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`code` {
        "email": "mariamavroeidi@gmail.com" ,
        "username": "mariamav",
        "password": "11111"    
    }

###/logout



###/searchFlight
###/bookFlight
###/searchBooking
###/cancelBooking
###/sortBookings
###/getBookingByDestination
###inactivateAccount
###/activateAccount



###/addAdmin
###/addFlight
###/updatePrice
###/deleteFlight
