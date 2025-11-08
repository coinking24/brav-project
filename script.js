// okay.html 페이지 스크립트
if (document.body.classList.contains('page-okay')) { 
    const productMainImage = document.getElementById('productMainImage'); 
    const colorSwatches = document.querySelectorAll('.page-okay .color-swatches .swatch'); 
    const colorSelect = document.getElementById('color-select');
    const giftSelect = document.getElementById('gift-card-select-okay'); 
    const giftText = document.getElementById('gift-message-text-okay'); 
    
    const leftArrow = document.querySelector('.page-okay .left-arrow');
    const rightArrow = document.querySelector('.page-okay .right-arrow');

    const imageSets = {
        black: ['okay3.png', 'okay4.png', 'okay2.png'],
        white: ['okay(white)3.png', 'okay(white)4.png', 'okay(white)2.png']
    };
    
    let currentImageIndex = 0; 
    let currentColor = 'black'; 

    function updateProductImage() {
        if (productMainImage && imageSets[currentColor]) {
            productMainImage.src = imageSets[currentColor][currentImageIndex];
            
            let altText = `Okay Hoodie ${currentColor} `;
            if (currentImageIndex === 0) altText += 'View 1 (Back)'; // okay3.png
            else if (currentImageIndex === 1) altText += 'View 2'; // okay4.png
            else if (currentImageIndex === 2) altText += 'View 3 (Side)'; // okay2.png
            productMainImage.alt = altText;
        }
    }

    if (leftArrow) {
        leftArrow.addEventListener('click', () => {
            currentImageIndex--;
            if (currentImageIndex < 0) {
                currentImageIndex = imageSets[currentColor].length - 1;
            }
            updateProductImage();
        });
    }

    if (rightArrow) {
        rightArrow.addEventListener('click', () => {
            currentImageIndex++;
            if (currentImageIndex >= imageSets[currentColor].length) {
                currentImageIndex = 0;
            }
            updateProductImage();
        });
    }

    if (colorSwatches.length > 0 && colorSelect) { 
        colorSwatches.forEach(swatch => {
            swatch.addEventListener('click', () => { 
                colorSwatches.forEach(s => s.classList.remove('active'));
                swatch.classList.add('active');
                
                currentColor = swatch.dataset.color; 
                colorSelect.value = currentColor;
                
                currentImageIndex = 0; 
                updateProductImage(); 
            });
        });

        colorSelect.addEventListener('change', (event) => {
            currentColor = event.target.value;
            colorSwatches.forEach(s => {
                s.classList.remove('active');
                if (s.dataset.color === currentColor) { 
                    s.classList.add('active');
                }
            });
            
            currentImageIndex = 0; 
            updateProductImage(); 
        });
    }

    if (giftSelect && giftText) {
        giftSelect.addEventListener('change', (event) => {
            // (내용 없음)
        });
    }
}

// (✅ 수정) keep.html 페이지 스크립트
if (document.body.classList.contains('page-keep')) {
    const productImageKeep = document.getElementById('productImageKeep');
    const productNameKeep = document.getElementById('productNameKeep');
    const productPriceKeep = document.getElementById('productPriceKeep');
    const typeSwatchesKeep = document.querySelectorAll('.page-keep .type-swatches .type-swatch');
    const colorSwatchesKeep = document.querySelectorAll('.page-keep .color-swatches .swatch'); 
    const colorSelectKeep = document.getElementById('color-select-keep');
    const productInfoWrapper = document.querySelector('.page-keep .product-info-wrapper'); 
    const productImageWrapper = document.querySelector('.page-keep .product-image-wrapper'); 
    const giftSelectKeep = document.getElementById('gift-card-select-keep'); 
    const giftTextKeep = document.getElementById('gift-message-text-keep'); 

    let currentKeepType = 'notebook'; 

    if (productImageKeep && productNameKeep && productPriceKeep && typeSwatchesKeep.length > 0 && colorSwatchesKeep.length > 0 && colorSelectKeep && productInfoWrapper && productImageWrapper && giftSelectKeep && giftTextKeep) {

        // 타입 스와치 클릭 이벤트 (버그 수정)
        typeSwatchesKeep.forEach(swatch => {
            swatch.addEventListener('click', () => { 
                currentKeepType = swatch.dataset.type; 

                typeSwatchesKeep.forEach(s => s.classList.remove('active'));
                swatch.classList.add('active');

                // (✅ 수정) 이 두 줄이 버그를 수정하는 핵심입니다.
                // 클릭할 때마다 스와치에 저장된 이름과 가격을 다시 불러옵니다.
                // (html에서 10,000원으로 수정했기 때문에 10,000원이 로드됨)
                productNameKeep.textContent = swatch.dataset.name;
                productPriceKeep.textContent = swatch.dataset.price;

                if (currentKeepType === 'pen') {
                    productImageKeep.src = swatch.dataset.image; 
                    productInfoWrapper.classList.add('pen-selected');
                    productImageWrapper.classList.add('pen-selected'); 
                } 
                else { // 'notebook'을 다시 클릭했을 때
                    productInfoWrapper.classList.remove('pen-selected');
                    productImageWrapper.classList.remove('pen-selected');
                    colorSelectKeep.value = 'white'; 
                    colorSelectKeep.dispatchEvent(new Event('change')); 
                }
            });
        });

        // 색상 스와치 마우스오버 이벤트
        colorSwatchesKeep.forEach(swatch => {
            swatch.addEventListener('mouseenter', () => {
                if (currentKeepType === 'notebook') { 
                    productImageKeep.src = swatch.dataset.image;
                    colorSwatchesKeep.forEach(s => s.classList.remove('active'));
                    swatch.classList.add('active');
                    colorSelectKeep.value = swatch.dataset.colorValue; 
                }
            });
        });

        // 색상 선택 드롭다운 변경 이벤트
        colorSelectKeep.addEventListener('change', (event) => {
            if (currentKeepType === 'notebook') { 
                const selectedColor = event.target.value;
                let newImage = '';
                if (selectedColor === 'white') {
                    newImage = 'keepwhite.png';
                } else if (selectedColor === 'gray') {
                    newImage = 'keepgray.png';
                }
                
                if (newImage) { 
                    productImageKeep.src = newImage;
                }
                
                colorSwatchesKeep.forEach(s => {
                    s.classList.remove('active');
                    if (s.dataset.colorValue === selectedColor) {
                        s.classList.add('active');
                    }
                });
            }
        });

        // 기프트 카드 선택
        giftSelectKeep.addEventListener('change', (event) => {
            // (내용 없음)
        });

        // 초기 로드 시 노트북 상태로 색상 설정
        if (currentKeepType === 'notebook') {
             colorSelectKeep.value = 'white'; 
             colorSelectKeep.dispatchEvent(new Event('change'));
        }

    } // end if elements exist
} 

// with.html 페이지 스크립트
if (document.body.classList.contains('page-with')) {
    const giftSelectWith = document.getElementById('gift-card-select-with'); 
    const giftTextWith = document.getElementById('gift-message-text-with'); 

    if (giftSelectWith && giftTextWith) {
        // 기프트 카드 선택
        giftSelectWith.addEventListener('change', (event) => {
            // (내용 없음)
        });
    }
}