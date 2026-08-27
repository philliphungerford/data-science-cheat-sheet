fGetMasterTable <- function(pDBConnection, pSQLFile, pSettings) {
  
  # Read the SQL query from the file
  Query <- read_file(pSQLFile)
  
  MasterTable <- dplyr::tbl(pDBConnection, sql(Query)) %>%
    dplyr::collect()
  
  return(MasterTable)
  
}