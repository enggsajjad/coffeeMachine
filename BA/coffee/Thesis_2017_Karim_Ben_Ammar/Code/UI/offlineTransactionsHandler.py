from dbHandler import updateDB, handleOfflineTransactions
from util import internet_on

if internet_on():
 handleOfflineTransactions()
 updateDB()

