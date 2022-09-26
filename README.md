# YpoxreotikiErgasiaSept22_E19098_Mavroeidi_Maria

Yποχρεωτική Εργασία Σεπτεμβρίου στο μάθημα Πληροφοριακά Συστήματα. 

##Περιγραφή της Εφαρμογής

Δημιουργία webservice για την υλοποίηση της υπηρεσίας DS Airlines.



##Προϋποθέσεις:

### Εγκατάσταση Docker.
 Μετά την εγκατάσταση του Docker Desktop Installer.exe Εντολή στο cmd:
`pip install docker docker-compose` 

Tο πρόγραμμα θα εκτελείται στην πόρτα 5000 μέσω flask και η Mongodb θα βρίσκεται στην πόρτα 27017.
Στην MongoDB δημιουργήθηκε μία database "DSAirlines" με collections users και flights.

Για την δημιουργία του container, κατεβάστε αυτό το directory και εκτελέστε:
`docker container create`





##Web Service: Λειτουργίες Απλού Χρήστη

###/signup
Δίνοντας 0.0.0.0:5000/signup με μέθοδο POST, μπορούμε να δημιουργείτε ένας χρήστη στο σύστημα. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
` {
        "email": "mariamavroeidi@gmail.com" ,
        "username": "mariamav",
        "fistname": "Maria",
        "lastname": "Mavroeidi",
        "password": "11111",
        "passport": "323232121",
        "category": "user"
    }`
To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή  και τότε γίνεται η δημιουργία του χρήστη. 
Αν υπάρχει χρήστης με ίδιο email ή passport,δεν θα γίνεται η εισαγωγή.

###/login
Δίνοντας 0.0.0.0:5000/login με μέθοδο POST, μπορεί ένας χρήστης να κάνει login στο σύστημα. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{
        "email": "mariamavroeidi@gmail.com" ,
        "username": "mariamav",
        "password": "11111"    
  }` 
To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή και τότε γίνεται η δημιουργία του χρήστη.
Αν το username δεν υπάρχει ή το password είναι λάθος ,δεν γίνεται login.
Αν γίνει login  το πρόγραμμα επιστρέφει το username μαζί με το μοναδικό uuid και ξεκινάει session.
Το uuid δημιουργείται κατά τo login, οπότε αλλάζει κάθε φορά που θα ξανακάνετε login στο πρόγραμμα.

###/logout
Δίνοντας 0.0.0.0:5000/logout με μέθοδο POST, μπορεί ένας χρήστης να κάνει logout απο στο σύστημα με αποτέλεσμα να τελειώσει το session.

###/searchFlight
Δίνοντας 0.0.0.0:5000/searchFlight με μέθοδο GET, μπορεί ένας χρήστης να αναζητήσει μια πτήση. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{
        "from": "city1" ,
        "to": "city2",
        "date": "date1"    
  }` 
To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή και τότε εμφανίζονται οι διαθέσιμες πτήσεις.
Αν δεν υπάρχουν πτήσεις με τα δεδομένα του json αρχείου ενημερώνεται ο χρήστης.

###/bookFlight
Δίνοντας 0.0.0.0:5000/searchFlight με μέθοδο POST, μπορεί ένας χρήστης να αναζητήσει μια πτήση. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{
   "flightID": "id1" ,
   "firstname": "name1",
   "lastname": "lastname1"    
   "passport": "passport1"  
   "card": "cardnumber1"  
 }` 
To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν δεν υπάρχουν πτήσεις με τα δεδομένα του json αρχείου ενημερώνεται ο χρήστης.

###/searchBooking
Δίνοντας 0.0.0.0:5000/searchBooking με μέθοδο GET, μπορεί ένας χρήστης να αναζητήσει μια πτήση με το μοναδικό id της πτήσης. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{"flightID": "id1" }`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν δεν βρεθεί κράτηση με τα δεδομένα του json αρχείου ενημερώνεται ο χρήστης.

###/cancelBooking
Δίνοντας 0.0.0.0:5000/cancelBooking με μέθοδο GET, μπορεί ένας χρήστης να αναζητήσει μια πτήση με το μοναδικό id της πτήσης. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{"flightID": "id1" }`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν δεν βρεθεί κράτηση με τα δεδομένα του json αρχείου δεν γίνεται η διαγραφή και ενημερώνεται ο χρήστης.


###/sortBookings
Δίνοντας 0.0.0.0:5000/sortBookings με μέθοδο GET, μπορεί ένας χρήστης εισάγει τρόπο ταξίνομησης (asc/desc) και να του εμφανιστόυν. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
i.`{"ored": "asc" }`
ii.`{"ored": "desc" }`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν δεν βρεθεί καμία κράτηση ενημερώνεται ο χρήστης.

###/getBookingByDestination
Δίνοντας 0.0.0.0:5000/sortBookings με μέθοδο GET, μπορεί ένας χρήστης κάνει αναζητήση στις κρατήσεις του με βάση τον προορισμό της πτήσης. Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{"to": "destinationExample" }`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν δεν βρεθεί καμία κράτηση ενημερώνεται ο χρήστης.

###inactivateAccount
Δίνοντας 0.0.0.0:5000/inactivateAccount με μέθοδο POST, μπορεί ένας χρήστης να κάνει κάνει απενεργοποιήση τον λογαριασμό του. Αφού απενεργοποιηθεί ο λογαριασμός, θα επιστρέφεται στο χρήστη
ένα μοναδικό συνθηματικό 12 χαρακτήρων το οποίο θα μπορεί να χρησιμοποιήσει μετέπειτα για την ενεργοποίηση του λογαριασμού.
Το session τελειώνει.


###/activateAccount
Δίνοντας 0.0.0.0:5000/activateAccount με μέθοδο POST, μπορεί ένας χρήστης να ξανα-ενεργοποιήσει τον λογαριασμό του με τον κωδικό ενεργοποίησης (που του είχε δωθεί κατά την απενεργοποίηση του λογιαρμού) . 
Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{"code": "codeExample" }`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν ο κωδικός ενεργοποίησης είναι λάθος, δεν γίνεται ενεργοποίηση του λογαριασμού και ενημερώνεται ο χρήστης.


##Web Service: Λειτουργίες Διαχειριστή

###/addAdmin
Δίνοντας 0.0.0.0:5000/addAdmin με μέθοδο POST, μπορεί ένας admin να εισάγει εναν καινούριο admin. 
Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{
   "email": "emailExample"
   "firstname": "firstnameExample"
   "lastname": "lastnameExample"
   "adminCode": "adminCodeExample"

}`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν υπάρχει άλλος χρήστης με το ίδιο email δεν γίνεται η εισαγωγή.
Αν το session δεν είναι admin session δεν γίνεται η εισαγωγή.


###/addFlight
Δίνοντας 0.0.0.0:5000/addFlight με μέθοδο POST, μπορεί ένας admin να εισάγει μια καινούρια πτήση. 
Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{
   "date": "dateExample"
   "from": "fromExample"
   "to": "toExample"
   "price": "priceExample"
   "hours": "hoursExample"

}`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν το session δεν είναι admin session δεν γίνεται η εισαγωγή.
Το πρόγραμμα δημιουργεί την id της πτήσης.

###/updatePrice
Δίνοντας 0.0.0.0:5000/updatePrice με μέθοδο POST, μπορεί ένας admin να αλλάξει την τιμή μιας πτήσης. 
Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{
   "flightID": "flightIDExample"
   "newPrice": "newPriceExample"
}`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν το session δεν είναι admin session δεν γίνεται η αλλαγή.
Aν η καινούρια τιμή δεν είναι μεγαλύτερη του μηδενός δεν γίνεται η αλλαγή.
Αν έχουν ξεκίνησει οι κράτησεις για την συγκεκριμένη πτήση δεν 


###/deleteFlight
Δίνοντας 0.0.0.0:5000/deleteFlight με μέθοδο POST, μπορεί ένας admin να διαγράψει μια πτήση. 
Ο χρήστης θα δοθεί ως ένα json αρχείο της μορφής:
`{"flightID": "flightIDExample"}`

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή.
Αν το session δεν είναι admin session δεν γίνεται η διαγραφή.


