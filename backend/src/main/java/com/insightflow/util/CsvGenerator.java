package com.insightflow.util;

import com.insightflow.model.Review;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.springframework.stereotype.Component;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.List;

@Component
public class CsvGenerator {

    public ByteArrayOutputStream generateCsv(List<Review> reviews) throws IOException {

        ByteArrayOutputStream out = new ByteArrayOutputStream();

        try (OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
                CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT
                        .builder()
                        .setHeader("review_id", "user_id", "product_id", "product_name", "store_id", "store_name",
                                "rating", "comment", "review_date")
                        .build())) {

            for (Review review : reviews) {
                printer.printRecord(
                        review.getReviewId(),
                        review.getUsers() != null ? review.getUsers().getUserId() : null,
                        review.getProduct() != null ? review.getProduct().getProductId() : null,
                        review.getProduct() != null ? review.getProduct().getProductName() : null,
                        review.getProduct() != null && review.getProduct().getStore() != null
                                ? review.getProduct().getStore().getStoreId()
                                : null,
                        review.getProduct() != null && review.getProduct().getStore() != null
                                ? review.getProduct().getStore().getStoreName()
                                : null,
                        review.getRating(),
                        review.getReviewText(),
                        review.getReviewDate());
            }
        }

        return out;
    }
}