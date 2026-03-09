package com.insightflow.service;


import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.insightflow.model.Review;
import com.insightflow.repository.ReviewRepository;
import com.insightflow.util.CsvGenerator;

import io.minio.BucketExistsArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ReviewExportService {

    private final ReviewRepository reviewRepository;
    private final CsvGenerator csvGenerator;
    private final MinioClient minioClient;

    @Value("${minio.bucket}")
    private String bucket;

    @Transactional(readOnly = true)
    public String exportReviews() throws Exception {

        List<Review> reviews = reviewRepository.findAll();
        System.out.println("Exporting " + reviews.size() + " reviews to CSV...");
        ByteArrayOutputStream outputStream = csvGenerator.generateCsv(reviews);

        String objectName = "reviews/reviews_" + System.currentTimeMillis() + ".csv";
        byte[] bytes = outputStream.toByteArray();

        // Ensure bucket exists
        boolean exists = minioClient.bucketExists(
                BucketExistsArgs.builder().bucket(bucket).build());
        if (!exists) {
            minioClient.makeBucket(
                    MakeBucketArgs.builder().bucket(bucket).build());
        }

        minioClient.putObject(
                PutObjectArgs.builder()
                        .bucket(bucket)
                        .object(objectName)
                        .stream(new ByteArrayInputStream(bytes), bytes.length, -1)
                        .contentType("text/csv")
                        .build()
        );

        return objectName;
    }
}