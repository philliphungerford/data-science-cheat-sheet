def get_ssms_connection():
    conn_str = (
        f"DRIVER={{{get_env('TARGET_DB_DRIVER', 'ODBC Driver 17 for SQL Server')}}};"
        f"SERVER={get_env('TARGET_DB_SERVER')},{get_env('TARGET_DB_PORT', '1433')};"
        f"DATABASE={get_env('TARGET_DB_NAME')};"
        f"UID={get_env('TARGET_DB_USER')};"
        f"PWD={get_env('TARGET_DB_PASSWORD')};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

conn = get_ssms_connection_nswcr()

 query = """
    SELECT COUNT(*) AS total_reports
    FROM Notification
    INNER JOIN NotificationPatient np
        ON Notification.NotificationId = np.NotificationId
    
    INNER JOIN NotificationCase
        ON Notification.NotificationId = NotificationCase.NotificationId
    
    INNER JOIN NotificationEpisode
        ON Notification.NotificationId = NotificationEpisode.NotificationId
    
    LEFT JOIN ReferenceItem sitecode
        ON sitecode.ReferenceItemId = CancerSiteCodeID
    
    LEFT JOIN ReferenceItem morphcode
        ON morphcode.ReferenceItemId = MorphologyCodeId
    
    LEFT JOIN ReferenceItem facility
        ON facility.Code = np.FacilityCode
       AND facility.ReferenceTypeId = 9
    
    LEFT JOIN ReferenceItem state
        ON state.ReferenceItemId = np.WayfareStateId
       AND state.ReferenceTypeId = 3
    
    WHERE NotificationEpisode.EpisodeStartDate >= '2000-01-01'
      AND NotificationSourceId = 6584
      AND Notification.DeletedFlag = 0
      AND NotificationStatusId != 6357
    """
        
result = pd.read_sql(query, conn)

# this is the df 
total_reports = result.iloc[0]["total_reports"]

    