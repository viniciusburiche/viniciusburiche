Sub ClearFilledData()

    ' Variable declaration
    Dim wsDFs As Worksheet
    Dim targetRows As Variant
    Dim i As Long

    ' Define the target worksheet
    Set wsDFs = Worksheets("DFs")

    ' Define the rows that need to be cleared
    targetRows = Array(59, 76, 124, 65, 67, 61, 82, 84, 86, 101, 94, 107, 110, 109, 117, _
                       69, 70, 74, 97, 98, 60, 83)

    ' Clear data in columns C, D, and E for the specified rows
    For i = LBound(targetRows) To UBound(targetRows)
        wsDFs.Range("C" & targetRows(i) & ":E" & targetRows(i)).ClearContents
    Next i

    ' Completion message
    MsgBox "Data has been successfully cleared!", vbInformation

End Sub
