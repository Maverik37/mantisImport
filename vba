Sub ExportExcelToJSON_Groupe()

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim lot As String, version As String
    Dim json As String
    Dim dict As Object, lotDict As Object, verDict As Object
    
    Dim analyseBrut As String, ancienneVer As String, analyseTexte As String
    
    Set ws = ThisWorkbook.Sheets("EnCours") ' <-- adapte le nom de l'onglet
    
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    Set dict = CreateObject("Scripting.Dictionary")
    
    For i = 2 To lastRow   ' ligne 1 = en-têtes
        
        ' --- Nom du Lot (colonne A) ---
        If Trim(ws.Cells(i, 1).Value) <> "" Then
            lot = Trim(ws.Cells(i, 1).Value)
            If Not dict.Exists(lot) Then
                Set lotDict = CreateObject("Scripting.Dictionary")
                dict.Add lot, lotDict
            Else
                Set lotDict = dict(lot)
            End If
        End If
        
        ' --- Version (colonne B) ---
        version = Trim(ws.Cells(i, 2).Value)
        If version <> "" Then
            Set verDict = CreateObject("Scripting.Dictionary")
            
            ' --- Découpage de la colonne Analyse (colonne D) ---
            analyseBrut = CStr(ws.Cells(i, 4).Value)
            If InStr(analyseBrut, "→") > 0 Then
                ' Ancienne version = avant le "→"
                ancienneVer = Trim(Split(analyseBrut, "→")(0))
                
                ' Analyse = texte entre parenthèses s'il y en a
                If InStr(analyseBrut, "(") > 0 And InStr(analyseBrut, ")") > 0 Then
                    analyseTexte = Mid(analyseBrut, InStr(analyseBrut, "(") + 1, InStr(analyseBrut, ")") - InStr(analyseBrut, "(") - 1)
                Else
                    analyseTexte = Trim(analyseBrut)
                End If
            Else
                ancienneVer = ""
                analyseTexte = analyseBrut
            End If
            
            ' --- Remplir dictionnaire version ---
            verDict.Add "Ancienne version", ancienneVer
            verDict.Add "Analyse", analyseTexte
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
    
    ' --- Boîte de dialogue pour enregistrer ---
    Dim fName As Variant
    fName = Application.GetSaveAsFilename( _
                InitialFileName:="export.json", _
                FileFilter:="Fichiers JSON (*.json), *.json", _
                Title:="Enregistrer sous...")
    
    If fName <> False Then
        Dim fso As Object, ts As Object
        Set fso = CreateObject("Scripting.FileSystemObject")
        Set ts = fso.CreateTextFile(fName, True, True)
        ts.Write json
        ts.Close
        MsgBox "Export terminé → " & fName
    Else
        MsgBox "Export annulé"
    End If
    
End Sub


' === Fonction récursive pour transformer dictionnaire en JSON ===
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
    
    If Right(tmp, 1) = "," Then tmp = Left(tmp, Len