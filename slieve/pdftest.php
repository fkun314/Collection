<?php

require('./tfpdf/tfpdf.php');
$pdf = new tFPDF;
$pdf->AddPage();
$pdf->AddFont('ShipporiMincho','','ShipporiMincho-TTF-Regular.ttf',true);
$pdf->SetFont('ShipporiMincho','',14);

-$pdf->Cell(40,10,'Hello World!');

+$pdf->Cell(40,10,'1+1=');
+$pdf->Cell(40,10,'1+2=');
+$pdf->Cell(40,10,'1+3=');

$pdf->Output();