package com.insightflow.service;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.insightflow.dto.FeedbackCategoryDto;
import com.insightflow.mapper.FeedbackCategoryMapper;
import com.insightflow.model.FeedbackCategory;
import com.insightflow.repository.FeedbackCategoryRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class FeedbackCategoryService {

    private final FeedbackCategoryRepository feedbackCategoryRepository;
    private final FeedbackCategoryMapper feedbackCategoryMapper;

    public List<FeedbackCategoryDto> findAll() {
        return feedbackCategoryRepository.findAll().stream()
                .map(feedbackCategoryMapper::toDto)
                .collect(Collectors.toList());
    }

    public FeedbackCategoryDto findById(Integer id) {
        FeedbackCategory category = feedbackCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Feedback category not found with id: " + id));
        return feedbackCategoryMapper.toDto(category);
    }

    public FeedbackCategoryDto findByCategoryName(String categoryName) {
        FeedbackCategory category = feedbackCategoryRepository.findByCategoryName(categoryName)
                .orElseThrow(() -> new RuntimeException("Feedback category not found with name: " + categoryName));
        return feedbackCategoryMapper.toDto(category);
    }

    public List<FeedbackCategoryDto> searchByName(String name) {
        return feedbackCategoryRepository.searchByName(name).stream()
                .map(feedbackCategoryMapper::toDto)
                .collect(Collectors.toList());
    }

    public FeedbackCategoryDto create(FeedbackCategoryDto dto) {
        if (feedbackCategoryRepository.existsByCategoryName(dto.getCategoryName())) {
            throw new RuntimeException("Category already exists with name: " + dto.getCategoryName());
        }
        FeedbackCategory category = feedbackCategoryMapper.toEntity(dto);
        return feedbackCategoryMapper.toDto(feedbackCategoryRepository.save(category));
    }

    public FeedbackCategoryDto update(Integer id, FeedbackCategoryDto dto) {
        FeedbackCategory category = feedbackCategoryRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Feedback category not found with id: " + id));
        feedbackCategoryMapper.updateEntityFromDto(dto, category);
        return feedbackCategoryMapper.toDto(feedbackCategoryRepository.save(category));
    }

    public void delete(Integer id) {
        if (!feedbackCategoryRepository.existsById(id)) {
            throw new RuntimeException("Feedback category not found with id: " + id);
        }
        feedbackCategoryRepository.deleteById(id);
    }

    public boolean existsByCategoryName(String categoryName) {
        return feedbackCategoryRepository.existsByCategoryName(categoryName);
    }
}
