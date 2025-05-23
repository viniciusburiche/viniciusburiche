Sub ImportData()

    Dim wsSource As Worksheet
    Dim wsTarget As Worksheet
    Dim searchKey As String
    Dim lastRow As Long
    Dim foundRow As Long

    Set wsSource = Worksheets("Source")
    Set wsTarget = Worksheets("Target")

    searchKey = wsTarget.Range("C7").Value

    If searchKey = "" Then
        MsgBox "C7 empty", vbExclamation
        Exit Sub
    End If

    lastRow = wsSource.Cells(wsSource.Rows.Count, "B").End(xlUp).Row

    On Error Resume Next
    foundRow = wsSource.Columns("B").Find(What:=searchKey, LookIn:=xlValues, LookAt:=xlWhole).Row
    On Error GoTo 0

    If foundRow = 0 Then
        MsgBox "data not found", vbExclamation
        Exit Sub
    End If

    Dim sourceColumns As Variant, targetRows As Variant
    sourceColumns = Array("F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", _
                          "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", _
                          "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", _
                          "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", _
                          "AZ", "BA", "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", _
                          "BK", "BL", "BM", "BN", "BO", "BP", "BQ", "BR", "BS")
    targetRows = Array(59, 59, 59, 76, 76, 76, 124, 124, 124, 65, 65, 65, 67, 67, 67, _
                       61, 61, 61, 82, 82, 82, 84, 84, 84, 86, 86, 86, 101, 101, 101, _
                       94, 94, 94, 107, 107, 107, 110, 110, 110, 109, 109, 109, 117, _
                       117, 117, 69, 69, 69, 70, 70, 70, 74, 74, 74, 97, 97, 97, 98, _
                       98, 98, 60, 60, 60, 83, 83, 83)

    Dim i As Long
    For i = LBound(sourceColumns) To UBound(sourceColumns) Step 3
        wsTarget.Cells(targetRows(i), "C").Value = wsSource.Cells(foundRow, sourceColumns(i)).Value
        wsTarget.Cells(targetRows(i), "D").Value = wsSource.Cells(foundRow, sourceColumns(i + 1)).Value
        wsTarget.Cells(targetRows(i), "E").Value = wsSource.Cells(foundRow, sourceColumns(i + 2)).Value
    Next i

    MsgBox "data imported.", vbInformation

End Sub
