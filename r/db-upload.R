fExportData <- function(x, pDBConWrite, pSettings, pTransformedData) {
  
  SplitDataFrameList0 <- base::split(
    pTransformedData[[x]],
    base::rep(1:base::ceiling(base::nrow(pTransformedData[[x]])/100000)*100000, each=100000)
  )
  
  # iterate over each batch and write to database
  # flag first chunk to identify when to load as new table
  isFirstChunk <- TRUE
  
  base::lapply(X = SplitDataFrameList0, FUN = function(df) {
    
    fWriteToDB(
      x = df, 
      pDBConWrite = pDBConWrite, 
      pSettings = pSettings, 
      pTableName = x, 
      clearTable = isFirstChunk
    )
    
    # assign to global, so it is picked up outside of function for the subsequent batches, so as to not overwrite. 
    isFirstChunk <<- FALSE
    
  })
  
  fPrintStatement(x, 2)
  
}

#

fWriteToDB <- function(x, pDBConWrite, pSettings, pTableName, clearTable = FALSE) {
  
  if (clearTable) {
    # Overwrite the existing table
    DBI::dbWriteTable(conn = pDBConWrite, name = pTableName, value = x, append = FALSE, overwrite = TRUE)
  } else {
    # Append to the existing table
    DBI::dbWriteTable(conn = pDBConWrite, name = pTableName, value = x, append = TRUE, overwrite = FALSE)
  }
  
}
