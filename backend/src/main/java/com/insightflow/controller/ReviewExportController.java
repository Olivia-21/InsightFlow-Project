package com.insightflow.controller;


import com.insightflow.service.ReviewExportService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/export")
public class ReviewExportController {

    @Autowired
    private ReviewExportService reviewExportService;

    @GetMapping("/reviews")
    public ResponseEntity<?> exportReviews() {

        try {

            String filePath = reviewExportService.exportReviews();

            return ResponseEntity.ok(
                    Map.of(
                            "message", "Reviews exported successfully",
                            "path", filePath
                    )
            );

        } catch (Exception e) {

            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Export failed", "details", e.getMessage() != null ? e.getMessage() : e.getClass().getSimpleName()));

        }
    }
}