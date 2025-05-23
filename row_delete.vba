Sub DeleteEmptyRows()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long

    Set ws = ThisWorkbook.Worksheets("Base de dados VP")

    lastRow = ws.Cells(ws.Rows.Count, "F").End(xlUp).Row

    For i = lastRow To 1 Step -1
        If IsEmpty(ws.Cells(i, "F")) Or IsEmpty(ws.Cells(i, "G")) Or IsEmpty(ws.Cells(i, "H")) Then
            ws.Rows(i).Delete
        End If
    Next i

    MsgBox "Rows deleted.", vbInformation
End Sub
