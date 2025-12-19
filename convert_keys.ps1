function ConvertPemToRsaPrivateXml {
    param([string]$pemPath)

    $pem = (Get-Content $pemPath -Raw) -replace "-----.*?-----",""
    $bytes = [Convert]::FromBase64String($pem)

    $rsa = [System.Security.Cryptography.RSA]::Create()
    $rsa.ImportRSAPrivateKey($bytes, [ref]0) | Out-Null
    return $rsa.ToXmlString($true)
}

function ConvertPemToRsaPublicXml {
    param([string]$pemPath)

    $pem = (Get-Content $pemPath -Raw) -replace "-----.*?-----",""
    $bytes = [Convert]::FromBase64String($pem)

    $rsa = [System.Security.Cryptography.RSA]::Create()
    $rsa.ImportSubjectPublicKeyInfo($bytes, [ref]0) | Out-Null
    return $rsa.ToXmlString($false)
}

ConvertPemToRsaPrivateXml "student_private.pem" | Set-Content "student_private.xml"
ConvertPemToRsaPublicXml "instructor_public.pem" | Set-Content "instructor_public.xml"
