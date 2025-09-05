Sub ExportExcelToJSON_Groupe()

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim lot As String, version As String
    Dim json As String
    Dim dict As Object, lotDict As Object, verDict As Object
    
    Set ws = ThisWorkbook.Sheets("EnCours") ' <-- adapte le nom si besoin
    
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    Set dict = CreateObject("Scripting.Dictionary")
    
    For i = 2 To lastRow   ' en supposant que ligne 1 = en-têtes
    
        ' Lire valeur dans Colonne A (Nom du Lot)
        If Trim(ws.Cells(i, 1).Value) <> "" Then
            ' c'est un "Lot principal"
            lot = Trim(ws.Cells(i, 1).Value)
            If Not dict.Exists(lot) Then
                Set lotDict = CreateObject("Scripting.Dictionary")
                dict.Add lot, lotDict
            Else
                Set lotDict = dict(lot)
            End If
        End If
        
        ' Si une version est renseignée en Colonne B
        version = Trim(ws.Cells(i, 2).Value)
        If version <> "" Then
            Set verDict = CreateObject("Scripting.Dictionary")
            
            verDict.Add "Ancienne version", ws.Cells(i, 3).Value
            verDict.Add "Analyse", ws.Cells(i, 4).Value
            verDict.Add "TicketInstallation", ws.Cells(i, 5).Value
            verDict.Add "Date d'analyse", ws.Cells(i, 6).Value
            verDict.Add "TicketOuvert", Split(CStr(ws.Cells(i, 7).Value), ",")
            verDict.Add "TicketFerme", Split(CStr(ws.Cells(i, 8).Value), ",")
            verDict.Add "Statut", ws.Cells(i, 9).Value
            verDict.Add "TRI", ws.Cells(i, 10).Value
            
            lotDict.Add version, verDict
        End If
    Next i
    
    json = DictToJSON(dict, 1)
    
    ' Sauvegarde dans un fichier JSON
    Dim fso As Object, ts As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set ts = fso.CreateTextFile(ThisWorkbook.Path & "\export.json", True, True)
    ts.Write json
    ts.Close
    
    MsgBox "Export terminé → " & ThisWorkbook.Path & "\export.json"

End Sub


' === Fonction récursive pour convertir dictionnaire en JSON ===
Function DictToJSON(d As Object, Optional indent As Integer = 0) As String
    Dim k As Variant
    Dim tmp As String, sp As String
    
    sp = String(indent * 4, " ")
    
    tmp = "{"
    For Each k In d.Keys
        tmp = tmp & vbCrLf & sp & """" & k & """:"
        If IsObject(d(k)) Then
            tmp = tmp & DictToJSON(d(k), indent + 1) & ","
        ElseIf IsArray(d(k)) Then
            tmp = tmp & "[""" & Join(d(k), """,""") & """],"
        Else
            tmp = tmp & """" & CStr(d(k)) & ""","
        End If
    Next
    
    If Right(tmp, 1) = "," Then tmp = Left(tmp, Len(tmp) - 1)
    tmp = tmp & vbCrLf & String((indent - 1) * 4, " ") & "}"
    
    DictToJSON = tmp
End Function