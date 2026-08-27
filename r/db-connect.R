fCreateDataConnection <- function(pDBName, pDBDriverName, pDBServerName, pDBPortNumber, pSettings) {
  
  
  # trusted_connection
  # The Trusted_Connection argument in an ODBC connection string is used to specify whether to use Windows Authentication
  # (also known as integrated security) to connect to the database. Setting Trusted_Connection to "yes" tells the system
  # to use the current Windows user credentials to authenticate with the database, rather than specifying a username (UID)
  # and password (PWD) explicitly.(also known as integrated security) to connect to the database. 
  # Setting Trusted_Connection to "yes" tells the system to use the current Windows user credentials to authenticate with the database,
  # rather than specifying a username (UID) and password (PWD) explicitly.
  
  if (is.null(pSettings$PWD)) {
    TrustedConnection <- "yes"
  } else {
    TrustedConnection <- "no"
  }
  
  dbConWrite <- DBI::dbConnect(odbc::odbc(), 
                               Driver = pDBDriverName,
                               Server = pDBServerName,                       
                               Database = pDBName, 
                               Port = pDBPortNumber,
                               Trusted_Connection = TrustedConnection,
                               UID = pSettings$UID,
                               PWD = pSettings$PWD
  )
  
}
