package com.insightflow.service;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.insightflow.dto.ReviewDto;
import com.insightflow.mapper.ReviewMapper;
import com.insightflow.model.Review;
import com.insightflow.repository.ReviewRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ReviewService {

    private final ReviewRepository reviewRepository;
    private final ReviewMapper reviewMapper;

    public List<ReviewDto> findAll() {
        return reviewRepository.findAll().stream()
                .map(reviewMapper::toDto)
                .collect(Collectors.toList());
    }

    public ReviewDto findById(Integer id) {
        Review review = reviewRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Review not found with id: " + id));
        return reviewMapper.toDto(review);
    }

    public List<ReviewDto> findByProductId(Integer productId) {
        return reviewRepository.findByProductProductId(productId).stream()
                .map(reviewMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<ReviewDto> findByUserId(Integer userId) {
        return reviewRepository.findByUsersUserId(userId).stream()
                .map(reviewMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<ReviewDto> findByRating(Integer rating) {
        return reviewRepository.findByRating(rating).stream()
                .map(reviewMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<ReviewDto> findByProductIdAndMinRating(Integer productId, Integer minRating) {
        return reviewRepository.findByProductIdAndMinRating(productId, minRating).stream()
                .map(reviewMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<ReviewDto> findByProductIdOrderByDate(Integer productId) {
        return reviewRepository.findByProductIdOrderByDateDesc(productId).stream()
                .map(reviewMapper::toDto)
                .collect(Collectors.toList());
    }

    public Double getAverageRatingForProduct(Integer productId) {
        return reviewRepository.getAverageRatingForProduct(productId);
    }

    public Long countByProductId(Integer productId) {
        return reviewRepository.countByProductId(productId);
    }

    public List<ReviewDto> findByStoreId(Integer storeId) {
        return reviewRepository.findByStoreId(storeId).stream()
                .map(reviewMapper::toDto)
                .collect(Collectors.toList());
    }

    public Double getAverageRatingForStore(Integer storeId) {
        return reviewRepository.getAverageRatingForStore(storeId);
    }

    public Long countByStoreId(Integer storeId) {
        return reviewRepository.countByStoreId(storeId);
    }

    public ReviewDto create(ReviewDto dto) {
        Review review = reviewMapper.toEntity(dto);
        return reviewMapper.toDto(reviewRepository.save(review));
    }

    public ReviewDto update(Integer id, ReviewDto dto) {
        Review review = reviewRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Review not found with id: " + id));
        reviewMapper.updateEntityFromDto(dto, review);
        return reviewMapper.toDto(reviewRepository.save(review));
    }

    public void delete(Integer id) {
        if (!reviewRepository.existsById(id)) {
            throw new RuntimeException("Review not found with id: " + id);
        }
        reviewRepository.deleteById(id);
    }
}
